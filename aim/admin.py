# aim.admin.py
from django.contrib import admin

from aim.models import *

class TransactionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Transaction, TransactionAdmin)

class HoldingAdmin(admin.ModelAdmin):
    model = Holding
admin.site.register(Holding, HoldingAdmin)

class HoldingInline(admin.TabularInline):
    model = Holding

class PortfolioAdmin(admin.ModelAdmin):
    pass
admin.site.register(Portfolio, PortfolioAdmin)

class SymbolAdmin(admin.ModelAdmin):
    search_fields = ['name']
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
