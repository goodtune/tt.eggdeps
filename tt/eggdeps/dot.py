# Copyright (c) 2007-2009 Thomas Lotze
# See also LICENSE.txt

import sys


def write_dot(graph, options, fp=None):
    """Print a dependency graph to a file-like object as a dot input file.

    graph: a tt.eggdeps.graph.Graph instance

    options: an object that provides formatting options as attributes

        cluster: bool, cluster direct dependencies of each root distribution?

        version_numbers: bool, print version numbers of active distributions?

        comment: str, optional, will be included at the top of the dot file

    fp: a file-like object, defaults to standard output if None
    """
    if fp is None:
        fp = sys.stdout

    if hasattr(options, 'comment'):
        for line in options.comment.splitlines():
            print >>fp, '// ' + line

    direct_deps = set()
    for name in graph.roots:
        direct_deps.update(graph[name])

    print >>fp, "digraph {"

    for node in graph.itervalues():
        node_options = {}
        if options.version_numbers and node.dist:
            node_options["label"] = "%s %s" % (node.name, node.dist.version)
        else:
            node_options["label"] = node.name

        def fill(color):
            node_options["style"] = "filled"
            node_options["fillcolor"] = color
        if node.name in direct_deps:
            fill("yellow")
        if node.name in graph.roots:
            fill("green")
        if not node.follow:
            fill("lightgrey")
        if not node.compatible:
            fill("red")

        print >>fp, '"%s"%s' % (node.name, format_options(node_options))

    if options.cluster:
        for i, cluster in enumerate(yield_clusters(graph)):
            print >>fp, "subgraph cluster_%s {" % i
            for name in cluster:
                print >>fp, '"%s"' % name
            print >>fp, "}"

    for node in graph.itervalues():
        for dep, extras in node.iter_deps():
            edge_options = {}
            if extras:
                edge_options["color"] = "lightgrey"

            print >>fp, '"%s" -> "%s"%s' % (node.name,
                                      dep, format_options(edge_options))

    print >>fp, "}"


def print_dot(graph, options):
    """Print a dependency graph to standard output as a dot input file.

    graph: a tt.eggdeps.graph.Graph instance

    options: an object that provides formatting options as attributes

        cluster: bool, cluster direct dependencies of each root distribution?

        version_numbers: bool, print version numbers of active distributions?

        comment: str, optional, will be included at the top of the dot file
    """
    return write_dot(graph, options)


def format_options(options):
    if not options:
        return ""

    return " [%s]" % ", ".join('%s="%s"' % item
                               for item in options.iteritems())


def yield_clusters(graph):
    clusters = [set(graph[name]).union((name,)) for name in graph.roots]
    while clusters:
        cluster = clusters.pop()
        for other in reversed(clusters):
            if cluster & other:
                cluster |= other
                clusters.remove(other)
        yield cluster
