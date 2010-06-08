from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.http import Http404

from aim.models import *
from aim.forms import *

def index(request):
    if request.user.is_authenticated():
        qs = Portfolio.objects.filter(owner=request.user)    
        # create a queryset of all public portfolios that I don't own.
        qs_public = Portfolio.objects.filter(permission = "V").exclude(owner=request.user)
    else:
        qs = Portfolio.objects.none()
        qs_public = Portfolio.objects.filter(permission = "V")
        
    template="aim/portfolio_list.html"
    
    return object_list(request,
                       queryset = qs,
                       template_name = template,
                       allow_empty=True,
                       extra_context={'public_list' : qs_public,},
                    )

#
#
# Portofolio's
#
#    
def portfolio(request, portfolio_id):
    return HttpResponse("View portfolio %s" % str(portfolio_id) )
    
def portfolio_add(request):

    # need to add Login_required stuff.

    if request.method == 'POST':
        form = PortfolioForm(request.POST) 
        if form.is_valid():            
            p = form.save(commit=False)
            p.owner = request.user
            p.save()
            
            return HttpResponseRedirect('/aim/') 
    else:
        form = PortfolioForm()

    return direct_to_template(request,
                              template='aim/portfolio_add.html',
                              extra_context = {'form' : form },
                            )
    
def portfolio_edit(request, portfolio_id):
    p = get_object_or_404(Portfolio, pk=portfolio_id)

    # make sure we own this portfolio
    if p.owner != request.user:
        raise Http404

    if request.method == 'POST':
        # find the portfolio in question
        form = PortfolioForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect('/aim/')
    else:
        form = PortfolioForm(instance=p)
    
    return direct_to_template(request,
                              template='aim/portfolio_add.html',
                              extra_context = {'form': form }
                            )

#
#
# Holdings
#
#
def holding_all(request):
    # show all holdings for a particular user    
    qs = Holding.objects.filter(portfolio__owner = request.user)

    return object_list(request,
                       queryset = qs,
                       template_name = 'aim/holding_all.html',
                       allow_empty=True,
                    )
#
# holding - show the detail of a holding
#
def holding(request, holding_id):
    obj = get_object_or_404(Holding, pk=holding_id)
    
    if obj.portfolio.owner != request.user:
        raise Http404

    return object_detail(request,
                         Holding.objects.all(),
                         object_id=holding_id,
                         template_name="aim/holding.html",
                        )
    
def holding_edit(request, holding_id):
    return HttpResponse("Edit Holding %s" % str(holding_id) )

def holding_add(request):
    # check to see if any parameters were passed
    port = None
    
    if "portfolio" in request.REQUEST:
        # first, can we find the portfolio in question
        port = get_object_or_404(Portfolio, pk=request.REQUEST['portfolio'])
        
        # and do we own this portfolio?
        if port.owner != request.user:
            raise Http404
    else:
        raise Http404
    
    if request.method == 'POST':
        form = HoldingForm(request.POST,)
        
        if form.is_valid():
            h = form.save()
            
            # jfm - add a AimValue control parameter record 1-1
            #av = Aim()
            #av.holding = h
            #av.save()            
            
            return HttpResponseRedirect('/aim/holding/%s' % str(h.id) )
    else:
        form = HoldingForm(initial={'portfolio':port.id})
        form['portfolio'].field.queryset = Portfolio.objects.filter(owner = request.user)
    
    return direct_to_template(request,
                              template='aim/holding_add.html',
                              extra_context = {'form': form }
                            )

#
#
# Misc. Functions
#
#
def aim_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/aim')
        else:
            return HttpResponseRedirect('/aim')
            # Return a 'disabled account' error message
    else:
        return HttpResponseRedirect('/')


