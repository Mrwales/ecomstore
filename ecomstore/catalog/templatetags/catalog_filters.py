from django import template
import locale
from decimal import Decimal

register=template.Library()
@register.filter(name='currency')

def currency(value):
    
    if isinstance(value, str):
        value=Decimal(value)
    try:
        locale.setlocale(locale.LC_ALL,'en_NG.UTF-8')
    except:
        locale.setlocale(locale.LC_ALL,'') #() -> dict. Returns numeric and monetary locale-specific  parameters.  international
    loc=locale.localeconv()
    
    return locale.currency(value, loc['currency_symbol'], grouping=True)



