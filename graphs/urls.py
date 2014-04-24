from django.conf.urls import patterns, include, url
from django.views.generic import ListView

from aim.models import Symbol

class graphview(ListView):
    template_name = "graphs/graphview.html"

    def get_queryset(self):
        return Symbol.objects.get(name=self.kwargs['symbol']).price_set.order_by('date')

class testgraphview(ListView):
    template_name = "graphs/testgraph.html"

    def get_context_data(self, **kwargs):
        cd = super(testgraphview, self).get_context_data(**kwargs)

        cd['symbol'] = self.kwargs['symbol']
        return cd

    def get_queryset(self):
        return Symbol.objects.get(name=self.kwargs['symbol']).price_set.all()

urlpatterns = patterns('',
    url(r'^(?P<symbol>\w+)/$', graphview.as_view() ),
    
    url(r'test/(?P<symbol>\w+)/$', testgraphview.as_view() ),
)