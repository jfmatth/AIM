from django import forms
from django.core.exceptions import ObjectDoesNotExist

from aim.models import AimBase, Portfolio, Holding, Transaction, Symbol

class ControlForm(forms.ModelForm):
    class Meta:
        model = AimBase
        fields = ('started', 'control',)
        
        
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



class HoldingForm(forms.ModelForm):
    # define symbol here to override the default ModelChoicefield dropdown list.
    symbol = forms.CharField()

    def __init__(self, user, portid, *args, **kwargs):
        super(HoldingForm,self).__init__(*args, **kwargs)
        # only show the portfolios for this user.
        self.fields['portfolio'].queryset = Portfolio.objects.filter(owner=user)
        self.fields['portfolio'].initial = portid

    def clean_symbol(self):
        # Since symbol needs to be a symbol object, use the clean
        # method to make sure it's valid, and if it is, return a symbol object, not the text.
        try:
            return Symbol.objects.get(name__iexact=self.cleaned_data['symbol'])
        except ObjectDoesNotExist:
            raise forms.ValidationError("Invalid symbol")

    class Meta:
        model = Holding
        fields = ('symbol', 'reason', 'portfolio' )


class TransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TransactionForm,self).__init__(*args, **kwargs)
        self.fields['holding'].initial = self.initial['holding_id']
        
    class Meta:
        model = Transaction
        fields = ('date', 'shares', 'price', 'holding', 'type' )
