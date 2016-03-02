from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.views.decorators import csrf
import json

from cart import cart
from cart.forms import ProductAddToCartForm as FProductAddToCartForm
from cart.models import ProductAddToCartForm
from catalog.forms import ProductReviewForm
from catalog.models import ProductReview
from ecomstore.settings import PRODUCTS_PER_ROW
from stats import stats
import tagging
from tagging.models import Tag, TaggedItem

from .models import Category, Product


# Create your views here.
def index(request):
    page_title = 'Musical Instruments and Sheet Music for Musicians'
    search_recs = stats.recommended_from_search(request)
    featured = Product.featured.all()[0:PRODUCTS_PER_ROW]
    recently_viewed = stats.get_recently_viewed(request)
    view_recs = stats.recommended_from_views(request)
    return render_to_response("catalog/index.html", locals(),context_instance=RequestContext(request))

def show_category(request, category_slug):
    c = get_object_or_404(Category, slug=category_slug)
    products = c.product_set.all()
    
    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    return render_to_response("catalog/category.html", locals(),context_instance=RequestContext(request))

def show_category_brands(request, category_slug,b_slug):
    c = get_object_or_404(Category, slug=category_slug)
    
    products = c.product_set.filter(b_slug=b_slug)

    page_title = b_slug
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    return render_to_response("catalog/brand.html", locals(),context_instance=RequestContext(request))

def show_product(request, product_slug):
    p = get_object_or_404(Product, slug=product_slug)
    categories = p.categories.filter(is_active=True)
    page_title = p.name
    meta_keywords = p.meta_keywords
    meta_description = p.meta_description
    
    # need to evaluate the HTTP method
    if request.method == 'POST':
        # add to cart...create the bound form
        postdata = request.POST.copy()
        form =ProductAddToCartForm(request.POST,instance=ProductAddToCartForm.cart_item)
        #check if posted data is valid
        if form.is_valid():
            cart_item =form.save(commit=False)
            #cart_item.cart_id = get_cart_id_function()
            cart_item.product = Product.objects.get(slug=product_slug)
            cart_item.save()
            message="added to cart"
            #add to cart and redirect to cart page
            cart.add_to_cart(request)
            # if test cookie worked, get rid of it
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            url = reverse('show_cart')
            return HttpResponseRedirect(url)
    else:
        form=FProductAddToCartForm()
    # assign the hidden input the product slug as the value
    #
    form.fields['product_slug'].widget.attrs['value']=product_slug
    # set the test cookie on our first GET request
    request.session.set_test_cookie()
    
    from stats import stats
    stats.log_product_view(request, p) # add to product view
    product_reviews = ProductReview.approved.filter(product=p).order_by('-date')
    review_form = ProductReviewForm()
    return render_to_response("catalog/product.html", locals(),context_instance=RequestContext(request))

@login_required
def add_review(request):
    form=ProductReviewForm(request.POST)
    if form.is_valid():
        review=form.save(commit=False)
        slug=request.POST.get('slug','')
        product=Product.active.get(slug=slug)
        review.user = request.user
        review.product = product
        review.save()
        
        context_dict={"review":review}
        #context_dict.update(csrf(request))
        
        html=render_to_string("catalog/product_review.html",context_dict)#which loads a template, renders it and returns the resulting string:
        
        response = json.dumps({'success':'True', 'html': html})
    else:
        html=form.errors.as_ul()
        response=json.dumps({'success':'False', 'html': html})
    return HttpResponse(response,content_type='application/javascript; charset=utf-8') #send it back to the jQuery function

@login_required
def add_tag(request):
    tags=request.POST.get('tag','')
    slug=request.POST.get('slug','')
    if len(tags)>2:
        p=Product.active.get(slug=slug)
        html=u''
        template='catalog/tag_link.html'
        for tag in tags.split():
            tag.strip(',')
            Tag.objects.add_tag(p,tag)
        for tag in p.tags:
            context_dict={'tag': tag }
            #context_dict.update(csrf(request))
            html += render_to_string(template, context_dict)
        response=json.dumps({'success':'True','html':html})
    else:
        response=json.dumps({'success':'False'})
    return HttpResponse(response,content_type='application/javascript; charset=utf8')

def tag_cloud(request):
    '''
     Obtain a list of tags associated with instances of the given
    Model, giving each tag a ``count`` attribute indicating how
    many times it has been used and a ``font_size`` attribute for
    use in displaying a tag cloud.
    
    ``steps`` defines the range of font sizes - ``font_size`` will
    be an integer between 1 and ``steps`` (inclusive).
    
    ``distribution`` defines the type of font size distribution
    algorithm which will be used - logarithmic or linear. It must
    be either ``tagging.utils.LOGARITHMIC`` or
    ``tagging.utils.LINEAR``.
    
    To limit the tags displayed in the cloud to those associated
    with a subset of the Model's instances, pass a dictionary of
    field lookups to be applied to the given Model as the
    ``filters`` argument.
    
    To limit the tags displayed in the cloud to those with a
    ``count`` greater than or equal to ``min_count``, pass a value
    for the ``min_count`` argument.
    """
    tags = list(self.usage_for_model(model, counts=True, filters=filters, 
            min_count=min_count))
    return calculate_cloud(tags, steps, distribution)
    '''
    product_tags = Tag.objects.cloud_for_model(Product, steps=9,
                                               distribution=tagging.utils.LOGARITHMIC,
                                               filters={ 'is_active': True })
    page_title = 'Product Tag Cloud'
    return render_to_response("catalog/tag_cloud.html",locals(),context_instance=RequestContext(request))
    
def tag(request,tag):
    products=TaggedItem.objects.get_by_model(Product.active, tag)
    return render_to_response("catalog/tag.html", locals(),context_instance=RequestContext(request))
    
    