from django.http.response import HttpResponse
from django.shortcuts import render
import os

from ecomstore.settings import BASE_DIR
from catalog.models import Product
from django.template.loader import get_template
from django.template.context import Context


# Create your views here.
ROBOTS_PATH=os.path.join(BASE_DIR,'marketing/robots.txt')

def robots(request):
    return HttpResponse(open(ROBOTS_PATH).read(), 'text/plain')

def google_base(request):
    products=Product.active.all()
    template=get_template("marketing/google_base.xml")
    xml=template.render(Context(locals()))
    return HttpResponse(xml,mimetype="text/xml")
