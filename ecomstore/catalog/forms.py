'''
Created on Jan 16, 2016

@author: wale
'''
from django import forms

from catalog.models import ProductReview

from .models import Product


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model =Product
        exclude=()
    
    def clean_price(self):
        if self.cleaned_data['price'] <= 0:
            raise forms.ValidationError('Price must be greater than zero.')
        return self.cleaned_data['price']
    
class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        exclude = ('user','product', 'is_approved')