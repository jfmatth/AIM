# aim.admin.py
from django.contrib import admin

from aim.models import *

class TransactionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Transaction, TransactionAdmin)

class HoldingAdmin(admin.ModelAdmin):
    list_display = ('stock', 'BuyPrice', 'SellPrice', 'CurrentPrice', 'shares', 'control', 'buyamount', 'sellamount')
    
    def BuyPrice(self, obj):
        return "%.2f" % obj.aim.BuyPrice()
        
    def SellPrice(self, obj):
        return "%.2f" % obj.aim.SellPrice()
        
    def CurrentPrice(self, obj):
        return "%.2f" % obj.stock.CurrentPrice()
        
    def shares(self, obj):
        return "%.2f" % obj.shares()
        
    def control(self, obj):
        return "%.2f" % obj.aim.control
    
    def buyamount(self, obj):
        return "%.2f" % obj.aim.BuyAmount()
        
    def sellamount(self, obj):
        return "%.2f" % obj.aim.SellAmount()
    
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
admin.site.register(AimStandard, AimAdmin)


