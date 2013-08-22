from django.forms import ModelForm
from aim.models import *

class PortfolioForm(ModelForm):

    class Meta:
        model = Portfolio
        fields = ['name', 'permission']

class HoldingForm(ModelForm):
    
    class Meta:
        model = Holding
