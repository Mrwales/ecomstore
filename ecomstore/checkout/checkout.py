'''
Created on Feb 6, 2016

@author: wale
'''
from django.core.urlresolvers import  reverse

import cart
from checkout.forms import CheckoutForm
from checkout.models import Order, OrderItem
from .authnet import  *
#from checkout.views import paypal_capture


def get_checkout_url(request):
    return reverse('checkout')

def process(request):
    #Transaction result
    
    APPROVED = '1'
    DECLINED = '2'
    ERROR = '3'
    HELD_FOR_REVIEW = '4'
    
    postdata = request.POST.copy()
    
    card_num = postdata.get('credit_card_number','')
    exp_month = postdata.get('credit_card_expire_month','')
    exp_year = postdata.get('credit_card_expire_year','')
    exp_date = exp_month + exp_year
    cvv = postdata.get('credit_card_cvv','')
    amount = cart.cart.cart_subtotal(request)
    results = {}
#     response =do_auth_capture(amount=amount,
#                             card_num=card_num,
#                             exp_date=exp_date,
#                             card_cvv=cvv
#                             )
#     
#for testing purposes
    response=[0]*6
    response[0]=APPROVED
    response[2]=1
    if response[0] == APPROVED:
        transaction_id = response[2]
        #transaction_id = response[6]
        order = create_order(request, transaction_id)
        results = {'order_number':order.id,'message':''}
    if response[0] == DECLINED:
        results = {'order_number':0,'message':'There is a problem with your credit card.'}
    if response[0] == ERROR or response[0] == HELD_FOR_REVIEW:
        results = {'order_number':0,'message':'Error processing your order.'}

    return results

def create_order(request,transaction_id):
    order=Order()
    checkout_form=CheckoutForm(request.POST,instance=order)
    order=checkout_form.save(commit=False)
    order.transaction_id= transaction_id
    order.ip_address = request.META.get('REMOTE_ADDR')
    order.user = None
    order.user = None
    if request.user.is_authenticated():
        order.user=request.user
    order.status = Order.SUBMITTED
    order.save()
    order.status = Order.SUBMITTED
    order.save()
    # if the order save succeeded
    if order.pk:
        cart_items = cart.cart.get_cart_items(request)
        for ci in cart_items:
        # create order item for each cart item
            oi = OrderItem()
            oi.order = order
            oi.quantity = ci.quantity
            oi.price = ci.price # now using @property
            oi.product = ci.product
            oi.save()
    # all set, empty cart
    cart.cart.empty_cart(request)
    #associate orders placed with registered users if they are logged in during the checkout process.
    if request.user.is_authenticated():
        from account import profile
        profile.set(request)
            # return the new order object
    return order
