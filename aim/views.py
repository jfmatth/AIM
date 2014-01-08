#from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from aim.forms import PortfolioForm, ControlForm, HoldingForm, TransactionForm

from aim.models import Portfolio, Holding, Symbol, Transaction, AimBase

#===============================================================================
# MainView for /aim
#===============================================================================
class MainView(ListView):
    """
    This is the main screen a logged in user sees for all their holdings and portfolios.
    """
    template_name = "aim/MainView.html"
    context_object_name = "object_list"

    def get_queryset(self):
        return Portfolio.objects.filter(owner=self.request.user)


#===============================================================================
# Portofolio's
#===============================================================================
class PortfolioUpdate(UpdateView):
    model = Portfolio
    success_url = "/aim/"
    form_class = PortfolioForm

class PortfolioCreate(CreateView):
    model = Portfolio
    form_class = PortfolioForm
    
    success_url = "/aim/"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(PortfolioCreate, self).form_valid(form)

    def get_initial(self):
        # save the user object for use in the Form
        self.initial.update( {'user' : self.request.user} )
        return super(PortfolioCreate, self).get_initial()


#===============================================================================
# Holding
#===============================================================================
class HoldingCreateView(CreateView):
    model = Holding
    form_class = HoldingForm
    success_url = "/aim/"

    template_name = "aim/HoldingView.html"

    def get_context_data(self, **kwargs):
        cd = super(HoldingCreateView,self).get_context_data(**kwargs)
        cd['newrecord'] = True
        
        return cd
    
    def get_form_kwargs(self):
        kwargs = super(HoldingCreateView,self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['portid'] = self.kwargs.get("portid", None)
        
        return kwargs 

class HoldingUpdateView(UpdateView):
    template_name = "aim/HoldingView.html"
    form_class = HoldingForm
    model = Holding
    success_url = "/aim/"
    queryset = Holding.objects.all()

    def get_form_kwargs(self):
        kwargs = super(HoldingUpdateView,self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['portid'] = self.kwargs.get("portid", None)
        
        return kwargs 

    def get_initial(self):
        # setup the symbol, otherwise it will show the FK id instead.
        initial = super(HoldingUpdateView, self).get_initial()
        initial.update({'symbol':self.object.symbol} )
        
        return initial
        

#===============================================================================
# Transaction
#===============================================================================
class TransactionCreate(CreateView):
    model = Transaction
    form_class = TransactionForm
    success_url = "/aim/"

    def get_initial(self):
        # save the user object for use in the Form
        self.initial.update( {'holding_id' : self.kwargs.get("holding_id", None) })
        
        return super(TransactionCreate,self).get_initial()
