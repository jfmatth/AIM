#from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django import forms

from django.views.generic.edit import CreateView, UpdateView
from django.core.exceptions import ObjectDoesNotExist

from aim.models import Portfolio, Holding, Symbol, Transaction

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


# Detail view for Holding
class HoldingView(DetailView):
    
    template_name = "aim/HoldingView.html"
    queryset = Holding.objects.all()

#===============================================================================
# Portofolio's
#===============================================================================
class PortfolioForm(forms.ModelForm):
    user = None
    
    class Meta:
        model = Portfolio
        exclude = ('owner',)
    
    def __init__(self, *args, **kwargs):
        super(PortfolioForm,self).__init__(*args, **kwargs)
        self.user = self.initial['user']
        
    def clean(self):
        # validate that this portfolio for this user doesn't already exist.
        
        try:
            Portfolio.objects.get(name=self.cleaned_data['name'], owner=self.initial['user'])
        except ObjectDoesNotExist:
            # record not found, OK.
            pass
        else:
            # no exception, meaning duplicate.
            raise forms.ValidationError('Portfolio with this Name already exists')
        
        return super(PortfolioForm,self).clean()
        
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
# Holding's (forms and views)
#===============================================================================
class HoldingForm(forms.ModelForm):
    # define symbol here to override the default ModelChoicefield dropdown list.
    symbol = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(HoldingForm,self).__init__(*args, **kwargs)
        # only show the portfolios for this user.
        self.fields['portfolio'].queryset = Portfolio.objects.filter(owner=self.initial['user'] )
        self.fields['portfolio'].initial = self.initial['portid']
        
    def clean_symbol(self):
        # Since symbol needs to be a symbol object, use the clean
        # method to make sure it's valid, and if it is, return a symbol object, not the text.
        try:
            return Symbol.objects.get(name__iexact=self.cleaned_data['symbol'])
        except ObjectDoesNotExist:
            raise forms.ValidationError("Invalid symbol")

    class Meta:
        model = Holding
        fields = ('symbol', 'portfolio' )

class HoldingCreate(CreateView):
    model = Holding
    form_class = HoldingForm
    success_url = "/aim/"

    def get_initial(self):
        # save the user object for use in the Form
        self.initial.update( {'user' : self.request.user} )
        self.initial.update( {'portid' : self.kwargs.get("portid", None) })
        
        return super(HoldingCreate,self).get_initial()


#===============================================================================
# Transaction's (forms and views)
#===============================================================================
class TransactionForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(TransactionForm,self).__init__(*args, **kwargs)
        self.fields['holding'].initial = self.initial['holding_id']
        
    class Meta:
        model = Transaction
        fields = ('date', 'shares', 'price', 'holding', 'type' )

class TransactionCreate(CreateView):
    model = Transaction
    form_class = TransactionForm
    success_url = "/aim/"

    def get_initial(self):
        # save the user object for use in the Form
        self.initial.update( {'holding_id' : self.kwargs.get("holding_id", None) })
        
        return super(TransactionCreate,self).get_initial()
