'''
Created on Feb 14, 2016

@author: wale
'''
from django import template
import urllib.parse

from search.forms import SearchForm


register=template.Library()


@register.inclusion_tag("tags/search_box.html")
def search_box(request):
    q = request.GET.get('q','')
    form = SearchForm({'q': q })
    return {'form': form }

@register.inclusion_tag('tags/pagination_links.html')
def pagination_links(request, paginator):
    raw_params = request.GET.copy()
    page = raw_params.get('page',1)
    p = paginator.page(page)
    try:
        del raw_params['page']
    except KeyError:
        pass
    params = urllib.parse.urlencode(raw_params)
    return {'request': request,
            'paginator': paginator,
            'p': p,
            'params': params }