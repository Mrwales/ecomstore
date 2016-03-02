from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core import urlresolvers
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template.context import RequestContext

from account import profile
from checkout.models import Order, OrderItem
from account.forms import UserprofileForm


# Create your views here.
def register(request,):
    if request.method == 'POST':
        postdata = request.POST.copy()
        # FORM PROVIDE BY DJANGO FOR REGISTERING New Users
        form = UserCreationForm(postdata)
        if form.is_valid():
            form.save()
            un = postdata.get('username','')
            pw = postdata.get('password1','')
            from django.contrib.auth import login, authenticate
            new_user = authenticate(username=un, password=pw)
            if new_user and new_user.is_active:#If the given credentials are valid, return a User object.
                login(request, new_user) 
                '''login() basically saves
you from having to call authenticate() every time you want to make sure the user is who they claim to
be, and lets you perform this check once, when they register or log in.'''
                url = urlresolvers.reverse('my_account')
                return HttpResponseRedirect(url)
    else:
        form = UserCreationForm()
    page_title = 'User Registration'
    return render_to_response("registration/register.html", locals(),context_instance=RequestContext(request))

@login_required
def my_account(request):
    page_title = 'My Account'
    orders = Order.objects.filter(user=request.user)
    name = request.user.username
    return render_to_response("registration/my_account.html", locals(),context_instance=RequestContext(request))

@login_required
def order_details(request, order_id, ):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    page_title = 'Order Details for Order #' + order_id
    order_items = OrderItem.objects.filter(order=order)
    return render_to_response("registration/order_details.html", locals(),context_instance=RequestContext(request))

@login_required
def order_info(request):
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = UserprofileForm(postdata)
        if form.is_valid():
            profile.set(request)
            url = urlresolvers.reverse('my_account')
            return HttpResponseRedirect(url)
    else:
        user_profile = profile.retrieve(request)
        form = UserprofileForm(instance=user_profile)
    page_title = 'Edit Order Information'
    return render_to_response("registration/order_info.html", locals(),context_instance=RequestContext(request))