#from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django import forms

from django.views.generic.edit import CreateView, UpdateView
from django.core.exceptions import ObjectDoesNotExist

from aim.models import Portfolio, Holding, Symbol

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
class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        exclude = ('owner',)    

class PortfolioUpdate(UpdateView):
    model = Portfolio
    success_url = "/aim/"
    form_class = PortfolioForm

class PortfolioCreate(CreateView):
    model = Portfolio
    form_class = PortfolioForm
    
#     template_name = 'aim/portfolio_add.html'
    success_url = "/aim/"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(PortfolioCreate, self).form_valid(form)

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
        
    def clean_symbol(self):
        # Since symbol needs to be a symbol object, use the clean
        # method to make sure it's valid, and if it is, return a symbol object, not the text.
        try:
            return Symbol.objects.get(name=self.cleaned_data['symbol'])
        except:
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
        return super(HoldingCreate,self).get_initial()
