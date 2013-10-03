
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^exchange', 'loader.views.LoadExchange'),
    url(r'^prices',   'loader.views.LoadPrices'),
    
    # upload a RAW .txt file to the form.
    url(r'^raw/exchange/(?P<exchange>\w+)',   'loader.views.ExchangeLoader'),
    url(r'^raw/prices/(?P<exchange>\w+)',   'loader.views.PricesLoader'),
    
    url(r'^$', 'loader.views.LoadAll'),
)