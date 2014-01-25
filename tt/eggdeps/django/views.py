# Copyright (c) 2014 Gary Reynolds
# See also LICENSE.txt

__author__ = 'gary@touch.asn.au'

import pygraphviz

from cStringIO import StringIO

from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.views.generic.base import View

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


class DigraphView(View):

    def get(self, request, *args, **kwargs):
        graph = Graph()
        graph.from_working_set()
        response = self.get_response(graph, *args, **kwargs)
        return response

    def get_response(self, graph, fmt='dot', *args, **kwargs):
        response = HttpResponse(mimetype=EXTENSION_MIME_MAP[fmt])
        write_dot(graph, Options(), response)
        return response


class DigraphImageView(DigraphView):

    shape= 'box'
    width = 3.0

    def get_response(self, graph, fmt='png', *args, **kwargs):
        fp = StringIO()
        write_dot(graph, Options(version_numbers=True), fp)
        fp.reset()

        site = Site.objects.get_current()
        response = HttpResponse(mimetype=EXTENSION_MIME_MAP[fmt])

        G = pygraphviz.AGraph(
            name=site.name, directed=True,
            rankdir='LR', rank='max', string=fp.read())

        G.node_attr['shape'] = self.shape
        G.node_attr['width'] = self.width
        G.draw(path=response, format=fmt, prog="dot")

        return response


digraph = DigraphView.as_view()
digraph_image = DigraphImageView.as_view()
