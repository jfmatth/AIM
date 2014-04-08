# aim.admin.py
from django.contrib import admin

from loader.models import Exchange, ExchangePrice, PriceError

class ExchangeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Exchange, ExchangeAdmin)

class ExchangePriceAdmin(admin.ModelAdmin):
    pass
admin.site.register(ExchangePrice, ExchangePriceAdmin)

class PriceErrorAdmin(admin.ModelAdmin):
    pass
admin.site.register(PriceError, PriceErrorAdmin)
