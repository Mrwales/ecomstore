'''
Created on Feb 13, 2016

@author: wale
'''
from django.db.models import Q

from catalog.models import Product
from search.models import SearchTerm



#from stats import stats
STRIP_WORDS = ['a','an','and','by','for','from','in','no','not',
'of','on','or','that','the','to','with']
#from ipware.ip import  get_ip
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def store(request,q):
    from stats import stats
    # if search term is at least three chars long, store in db
    if len(q) > 2:
        term = SearchTerm()
        term.q = q
        #term.ip=get_ip(request)
        term.ip_address = get_client_ip(request)
        term.tracking_id = stats.tracking_id(request)
        term.user = None
        if request.user.is_authenticated():
            term.user = request.user
        term.save()
    
# get products matching the search text
def products(search_text):
    words = _prepare_words(str(search_text))
    products = Product.active.all()
    results = {}
    results['products'] = []
    # iterate through keywords
    for word in words:
        #Q objects, which permits you to make the same type of queries using the icontains keywords, but gives you the option of which operator  to use
        products = products.filter(Q(name__icontains=word) |
                                   Q(description__icontains=word) |
                                    Q(sku__iexact=word) |
                                    Q(brand__icontains=word) |
                                    Q(meta_description__icontains=word) |
                                    Q(meta_keywords__icontains=word))
        results['products'] = products
    return results
                                
# strip out common words, limit to 5 words
def _prepare_words(search_text):
    words = search_text.split()
    for common in STRIP_WORDS:
        if common in words:
            words.remove(common)
    return words[0:5]