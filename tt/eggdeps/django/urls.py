__author__ = 'gary@touch.asn.au'

from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',

    url(r'^dependency.dot$',
        'tt.eggdeps.django.views.digraph',
        name='digraph-dot'),

    url(r'^dependency.(?P<fmt>(png|svg|jpg|pdf))$',
        'tt.eggdeps.django.views.digraph_image',
        name='digraph-image'),
)
