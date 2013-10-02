# aim.admin.py
from django.contrib import admin

from aim.models import Transaction, Holding, Symbol, Price, Portfolio, AimController, HoldingAlert

class TransactionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Transaction, TransactionAdmin)


def HoldingAdmin_currentprice(obj):
    if obj.symbol.currentprice:
        return obj.symbol.currentprice
    else:
        return 0
    
HoldingAdmin_currentprice.short_description = "Current Price"
def HoldingAdmin_alert(obj):
    if (obj.symbol.currentprice and obj.currentalert) and obj.symbol.currentprice > obj.currentalert.sellprice:
        return "SELL"
     
    if (obj.symbol.currentprice and obj.currentalert) and obj.symbol.currentprice < obj.currentalert.buyprice:
        return "BUY"
     
    return None
HoldingAdmin_alert.short_description = "Alert"

class HoldingAdmin(admin.ModelAdmin):
    model = Holding
    readonly_fields = ('currentalert',)
    list_display = ('symbol', 'currentalert', HoldingAdmin_currentprice, HoldingAdmin_alert)
admin.site.register(Holding, HoldingAdmin)

class HoldingInline(admin.TabularInline):
    model = Holding

class PortfolioAdmin(admin.ModelAdmin):
    pass
admin.site.register(Portfolio, PortfolioAdmin)

class SymbolAdmin(admin.ModelAdmin):
    search_fields = ['name']
    readonly_fields = ("currentprice",)
    list_display = ('name', 'description', 'currentprice',)
admin.site.register(Symbol, SymbolAdmin)

class PriceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Price, PriceAdmin)

class AimAdmin(admin.ModelAdmin):
    pass
admin.site.register(AimController, AimAdmin)

class AlertAdmin(admin.ModelAdmin):
    pass
admin.site.register(HoldingAlert, AlertAdmin)
