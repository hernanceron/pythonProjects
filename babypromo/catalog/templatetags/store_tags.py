from django import template

register = template.Library()

from ..models import Store

@register.inclusion_tag('catalog/active_stores.html')
def show_active_stores():
    active_stores = Store.objects.all().filter(status = 'ACT').order_by('name')
    return {'active_stores' : active_stores}