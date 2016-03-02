'''
Created on Feb 14, 2016

@author: wale
'''
from django import forms

from search.models import SearchTerm


class SearchForm(forms.ModelForm):
    class Meta:
        model = SearchTerm
        exclude=()
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        default_text = 'Search'
        self.fields['q'].widget.attrs['value'] = default_text
        self.fields['q'].widget.attrs['onfocus'] ="if (this.value=='" + default_text + "')this.value = ''"
    
    
    