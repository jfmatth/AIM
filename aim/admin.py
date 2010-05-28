# aim.admin.py
from django.contrib import admin

from aim.models import *

class TransactionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Transaction, TransactionAdmin)

class HoldingAdmin(admin.ModelAdmin):
    list_display = ('stock', 'nextbuy', 'nextsell', 'pricenow', 'shares')
    
    def nextbuy(self, obj):
        return "%.2f" % obj.NextBuy()
        
    def nextsell(self, obj):
        return "%.2f" % obj.NextSell()
        
    def pricenow(self, obj):
        return "%.2f" % obj.stock.current_price()
        
    def shares(self, obj):
        return "%.2f" % obj.shares()
    
    
admin.site.register(Holding, HoldingAdmin)

class HoldingInline(admin.TabularInline):
    model = Holding

class PortfolioAdmin(admin.ModelAdmin):
    #list_display = ('name', )
    #list_editable = ('name',)
    inlines = [ HoldingInline, ]
admin.site.register(Portfolio, PortfolioAdmin)


class StockAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Stock, StockAdmin)


class PriceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Price, PriceAdmin)

class AimAdmin(admin.ModelAdmin):
    pass
admin.site.register(Aim, AimAdmin)


