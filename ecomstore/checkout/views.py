
from django import forms
from django.core import urlresolvers
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext

from account import profile
import cart
import checkout
from checkout.forms import CheckoutForm
from checkout.models import OrderItem, Order


#from paypal.standard.forms import PayPalPaymentsForm
# Create your views here.
def show_checkout(request):
    if cart.cart.is_empty(request):
        cart_url = urlresolvers.reverse('show_cart')
        return HttpResponseRedirect(cart_url)
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = CheckoutForm(postdata)
        if form.is_valid():
            response = checkout.checkout.process(request)
            order_number = response.get('order_number',0)
            error_message = response.get('message','')
            if order_number:
                request.session['order_number'] = order_number
                receipt_url = urlresolvers.reverse('receipt')
                return HttpResponseRedirect(receipt_url)
            else:
                error_message = 'no order no'
                raise forms.ValidationError(error_message)
        else:
            error_message ='Correct the errors below'
    else:
        if request.user.is_authenticated():
            user_profile = profile.retrieve(request)
            form = CheckoutForm(instance=user_profile)
        else:
            form = CheckoutForm()
    page_title = 'Checkout'
    return render_to_response('checkout/checkout.html', locals(),context_instance=RequestContext(request))

def receipt(request):
    order_number = request.session.get('order_number','')
    if order_number:
        order = Order.objects.filter(id=order_number)[0]
        order_items = OrderItem.objects.filter(order=order)
        del request.session['order_number']
    else:
        cart_url = urlresolvers.reverse('show_cart')
        return HttpResponseRedirect(cart_url)
    return render_to_response('checkout/receipt.html',locals(), context_instance=RequestContext(request))



# def paypal_capture(request,amount='0.00', card_num=None, exp_date=None,card_cvv=None):
#     
#     # What you want the button to do.
#     paypal_dict = {
#         "business": settings.PAYPAL_RECEIVER_EMAIL,
#         "amount": amount,
#         "item_name": "name of the item",
#         "invoice": "unique-invoice-id","10000000.00"
#         "notify_url": "https://www.example.com" + reverse('paypal-ipn'),
#         "return_url": "https://www.example.com/your-return-location/",
#         "cancel_return": "https://www.example.com/your-cancel-location/",
#         "custom": "Upgrade all users!",  # Custom command to correlate to some function later (optional)
#     }
#     
#     # Create the instance.
#     form = PayPalPaymentsForm(initial=paypal_dict)
#     context = {"form": form}
#     
#     return render(request, "payment.html", context)