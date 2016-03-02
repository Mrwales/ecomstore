from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import  render_to_response

from search import search
from django.template.context import RequestContext


# Create your views here.
def results(request):
    q = request.GET.get('q', '')
    # get current page number. Set to 1 is missing or invalid
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page=1
    
    matching = search.products(q).get('products')
    # generate the pagintor object
    paginator = Paginator(matching,settings.PRODUCTS_PER_PAGE)
    
    try:
        results = paginator.page(page).object_list #list of matching products
    except (InvalidPage, EmptyPage):
        results = paginator.page(1).object_list
        
    search.store(request, q)

    page_title = 'Search Results for: ' + q
    return render_to_response("search/results.html", locals(),context_instance=RequestContext(request))