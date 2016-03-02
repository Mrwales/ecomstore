from decimal import Decimal
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

from catalog.models import Product


# Create your models here.

class BaseOrderInfo(models.Model):
    class Meta:
        abstract=True
    
    phone=models.CharField(max_length=20)
    email=models.EmailField(max_length=50)
    
    # shipping information
    shipping_name = models.CharField(max_length=50)
    shipping_address_1 = models.CharField(max_length=50)
    shipping_address_2 = models.CharField(max_length=50, blank=True)
    shipping_city = models.CharField(max_length=50)
    shipping_state = models.CharField(max_length=2)
    shipping_country = models.CharField(max_length=50)
    shipping_zip = models.CharField(max_length=10)

    # billing information
    billing_name = models.CharField(max_length=50)
    billing_address_1 = models.CharField(max_length=50)
    billing_address_2 = models.CharField(max_length=50, blank=True)
    billing_city = models.CharField(max_length=50)
    billing_state = models.CharField(max_length=2)
    billing_country = models.CharField(max_length=50)
    billing_zip = models.CharField(max_length=10)
    
class Order(BaseOrderInfo):
    # each individual status
    SUBMITTED = 1
    PROCESSED = 2
    SHIPPED = 3
    CANCELLED = 4
    
    # set of possible order statuses
    ORDER_STATUSES = (
                      (SUBMITTED,'Submitted'),(PROCESSED,'Processed'),
                      (SHIPPED,'Shipped'),(CANCELLED,'Cancelled'),
                    )
    
    # order info
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED)
    ip_address = models.GenericIPAddressField()
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True)
    transaction_id = models.CharField(max_length=20)
    
    
    def __str__(self):
        return 'Order #' + str(self.id)
    
    def get_absolute_url(self):
        return reverse('order_details',args=[str(self.id)])
    
    @property
    def total(self):
        total =Decimal('0.00')
        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            total += item.total
        return total
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=9,decimal_places=2)
    order = models.ForeignKey(Order)
    
    @property
    def total(self):
        return self.quantity * self.price
    
    @property
    def name(self):
        return self.product.name

    @property
    def sku(self):
        return self.product.sku
    
    def __str__(self):
        return self.product.name + ' (' + self.product.sku + ')'
    
    def get_absolute_url(self):
        return self.product.get_absolute_url()