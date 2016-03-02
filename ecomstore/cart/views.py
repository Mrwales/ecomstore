
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from checkout import checkout

from . import cart



# Create your views here
def show_cart(request):
    if request.method=="POST":
        if request.POST['submit']=="Remove":
            cart.remove_from_cart(request)
        if request.POST['submit']=="Update":
            cart.update_cart(request)
        if request.POST['submit']=='Checkout':
            checkout_url = checkout.get_checkout_url(request)
            return HttpResponseRedirect(checkout_url)
    cart_items=cart.get_cart_items(request)
    cart_subtotal = cart.cart_subtotal(request)
    page_title = 'Shopping Cart'
    return render_to_response('cart/cart.html',locals(),context_instance=RequestContext(request))
