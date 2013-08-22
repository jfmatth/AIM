# aim.admin.py
from django.contrib import admin

from loader.models import Exchange, ExchangePrice

class ExchangeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Exchange, ExchangeAdmin)

class ExchangePriceAdmin(admin.ModelAdmin):
    pass
admin.site.register(ExchangePrice, ExchangePriceAdmin)

