from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

import tagging
from tagging.registry import register

from .myThumbs import ThumbnailImageField


# Create your models here.
GENDERS=(
        ('UX', 'unisex'),
        ('M', 'men'),
        ('F', 'Female'),
        )
class ActiveCategoryManager(models.Manager):
    def get_queryset(self):
        return super(ActiveCategoryManager, self).get_queryset().filter(is_active=True)

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True,
                            help_text='Unique value for product page URL, created from name.')
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField("Meta Keywords",max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField("Meta Description", max_length=255,
                                        help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    active = ActiveCategoryManager()
    
    class Meta:
        db_table = 'categories'
        ordering = ['-created_at']
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('catalog_category',args=[str(self.slug)])
    
# class ActiveBrandManager(models.Manager):
#     def get_queryset(self):
#         return super(ActiveCategoryManager, self).get_queryset().filter(is_active=True)
# 
# class Brand(models.Model):
#     name = models.CharField(max_length=50)
#     slug = models.SlugField(max_length=50, unique=True,
#                             help_text='Unique value for product page URL, created from name.')
#     description = models.TextField()
#     is_active = models.BooleanField(default=True)
#     meta_keywords = models.CharField("Meta Keywords",max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag')
#     meta_description = models.CharField("Meta Description", max_length=255,
#                                         help_text='Content for description meta tag')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     
#     objects = models.Manager()
#     active = ActiveBrandManager()
#     
#     class Meta:
#         db_table = 'brands'
#         ordering = ['-created_at']
#         
#     def __str__(self):
#         return self.name
#     
#     def get_absolute_url(self):
#         return reverse('category_brand',args=[str(self.slug)])
        
class ActiveProductManager(models.Manager):
    #only the active records
    def get_queryset(self):
        return super(ActiveProductManager, self).get_queryset().filter(is_active=True)
    
class FeaturedProductManager(models.Manager):
    def all(self):
        return super(FeaturedProductManager, self).all().filter(is_active=True).filter(is_featured=True)
    

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True,
                            help_text='Unique value for product page URL, created from name.')
    
    brand = models.CharField(max_length=255,null=True)
    b_slug = models.SlugField(max_length=255,null=True)
    
    sku = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=9,decimal_places=2)
    old_price = models.DecimalField(max_digits=9,decimal_places=2,blank=True,default=0.00)
    #image = models.CharField(max_length=50)
    image =models.ImageField(upload_to='images/products/main')
    thumbnail = ThumbnailImageField(upload_to='images/products/thumbnails',thumb_width=125,thumb_height=125,default='')
    thumbnail1 = ThumbnailImageField(upload_to='images/products/thumbnails',thumb_width=125,thumb_height=125,null=True)
    thumbnail2 = ThumbnailImageField(upload_to='images/products/thumbnails',thumb_width=125,thumb_height=125,null=True)
    
    is_active = models.BooleanField(default=True)
    is_featured=models.BooleanField(default=False)
    
    gender=models.CharField(max_length=20,choices=GENDERS)
    
    quantity = models.IntegerField()
    description = models.TextField()
    meta_keywords = models.CharField(max_length=255,help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField(max_length=255,help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)
    
    objects = models.Manager()
    active = ActiveProductManager()
    featured=FeaturedProductManager()
    
    class Meta:
        db_table = 'products'
        ordering = ['-created_at']
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('catalog_product',args=[str(self.slug)])

    @property
    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None
    
    #Order-Based Filtering    
    def cross_sell(self):
        from checkout.models import Order,OrderItem
        orders=Order.objects.filter(orderitem__product=self)#where product is in  orderitem.products
        order_items=OrderItem.objects.filter(order__in=orders).exclude(product=self)#get other items excluding the presect product in the same order
        products=Product.active.filter(orderitem__in=order_items).distinct() #get the active ones removing duplicates
        return products
    
    #Customer-Based Order Filtering
    def cross_sell_user(self):
        from checkout.models import Order,OrderItem
        from django.contrib.auth.models import User
        users=User.objects.filter(order__orderitem__product=self)#get the users who made the order
        items=OrderItem.objects.filter(order__user__in=users).exclude(product=self) #list of other items ordered by same user
        products = Product.active.filter(orderitem__in=items).distinct()
        return products
        
    def cross_sell_hybrid(self):
        from checkout.models import Order,OrderItem
        from django.contrib.auth.models import User
        from django.db.models import Q
        orders=Order.objects.filter(orderitem__product=self)
        users=User.objects.filter(order__orderitem__product=self)
        items=OrderItem.objects.filter(Q(order__in=orders)|Q(order__user__in=users)).exclude(product=self)
        products = Product.active.filter(orderitem__in=items).distinct()
        #print(products)
        return products

try:
    register(Product)
except tagging.registry.AlreadyRegistered:
    pass
    
class ActiveProductReviewManager(models.Manager):
    def all(self):
        return super(ActiveProductReviewManager, self).all().filter(is_approved=True)
    
class ProductReview(models.Model):
    RATINGS = ((5,5),(4,4),(3,3),(2,2),(1,1),)
    
    product=models.ForeignKey(Product)
    user=models.ForeignKey(User)
    title=models.CharField(max_length=50)
    date=models.DateTimeField(auto_now_add=True)
    rating=models.PositiveSmallIntegerField(default=5,choices=RATINGS)
    is_approved=models.BooleanField(default=True)
    content=models.TextField()
    
    objects=models.Manager()
    approved=ActiveProductReviewManager()
    