 # aim.urls.py
 
from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required

from aim.views import MainView, PortfolioUpdate, PortfolioCreate, HoldingCreate, TransactionCreate

urlpatterns = patterns('',
    url(r'^$',
        login_required(MainView.as_view() ),
        name = "main"
    ),

    # Portfolio URL's
    url(r'^portfolio/(?P<pk>\d+)/$',
        login_required(PortfolioUpdate.as_view()),
        name = "portfolio_edit" ),
#     url(r'^portfolio/edit/(?P<pk>\d+)/$',
#         login_required(PortfolioUpdate.as_view()) ),
    url(r'^portfolio/add/$',
        login_required(PortfolioCreate.as_view()),
        name = "portfolio_add" ),

    url(r'^holding/add/(?P<portid>\d+)/$',
        login_required(HoldingCreate.as_view()),
        name = "holding_add"),
                       
    url(r'^holding/add/$',
        login_required(HoldingCreate.as_view()),
        name = "holding_addplain"),
                       
    url(r'^transaction/(?P<holding_id>\d+)/$',
        login_required(TransactionCreate.as_view() ),
        name = "transaction"),
                       
#     (r'^portfolio/add/$',                          'aim.views.portfolio_add'),
#     (r'^portfolio/edit/(?P<portfolio_id>\d+)/$',   'aim.views.portfolio_edit'),
    
    # Holdings
#     (r'^holding/all/$',                            'aim.views.holding_all'),
#     (r'^holding/(?P<holding_id>\d+)/$',            'aim.views.holding'),
#     (r'^holding/add/$',                            'aim.views.holding_add'),
#     (r'^holding/edit/(?P<holding_id>\d+)/$',       'aim.views.holding_edit'),
    
)
