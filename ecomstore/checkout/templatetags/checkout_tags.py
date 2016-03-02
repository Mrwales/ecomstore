'''
Created on Feb 8, 2016

@author: wale
'''

from django import template

register = template.Library()

@register.inclusion_tag("tags/form_table_row.html")
def form_table_row(form_field):
    return {'form_field': form_field }