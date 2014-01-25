# Copyright (c) 2014 Gary Reynolds
# See also LICENSE.txt

__author__ = 'gary@touch.asn.au'

import pygraphviz

from cStringIO import StringIO

from django.http import HttpResponse

from tt.eggdeps.dot import write_dot
from tt.eggdeps.graph import Graph
from tt.eggdeps.utils import Options

EXTENSION_MIME_MAP = {
    'dot': 'text/vnd.graphviz',
    'jpg': 'image/jpeg',
    'pdf': 'application/pdf',
    'png': 'image/png',
    'svg': 'image/svg+xml',
}


# TODO move to class based views, much is common and we should extract that all out.

def digraph(request):
    graph = Graph()
    graph.from_working_set()

    fmt = 'dot'
    response = HttpResponse(mimetype=EXTENSION_MIME_MAP[fmt])

    write_dot(graph, Options(), response)
    return response


def digraph_image(request, fmt="png"):
    graph = Graph()
    graph.from_working_set()

    s = StringIO()
    write_dot(graph, Options(version_numbers=True), s)
    s.reset()

    response = HttpResponse(mimetype=EXTENSION_MIME_MAP[fmt])

    G = pygraphviz.AGraph(name="xyz", directed=True, rankdir='LR', rank='max', string=s.read())
    G.node_attr['shape'] = 'box3d'
    G.node_attr['width'] = 3.0
    G.draw(path=response, format=fmt, prog="dot")

    return response
