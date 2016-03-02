'''
Created on Jan 28, 2016

@author: wale
'''

from django import template
from catalog.models import Category, Product
from cart import cart

register = template.Library()
@register.inclusion_tag("tags/cart_box.html")
def cart_box(request):
    cart_subtotal=cart.cart_subtotal(request)
    cart_item_count = cart.cart_distinct_item_count(request)
    return locals()

@register.inclusion_tag("tags/category_list.html")
def category_list(request_path):
    active_categories=Category.active.filter(is_active=True)
    return {
            'active_categories': active_categories,
            'request_path': request_path
            }



# @register.inclusion_tag("tags/brand_list.html")
# def brand_list():
#     c=Category.active.filter(is_active=True)
#     products=Product.objects.filter(categories=c)
#     return {
#             'products': products,
#             #'request_path': request_path
#             }

@register.inclusion_tag("tags/products_list.html")
def product_list(products, header_text):
    return { 'products': products,
            'header_text': header_text }
