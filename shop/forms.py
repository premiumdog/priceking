from django import forms
from django.forms import ModelForm
from .models import Product

class AffiliateLinkForm(ModelForm):

    class Meta:
        model = Product
        fields = ['product_id','user','product_price','product_name','product_link']
        widgets = {'product_id': forms.HiddenInput(), 'user': forms.HiddenInput(), 'product_price': forms.HiddenInput(), 'product_name': forms.HiddenInput(), 'product_link': forms.HiddenInput(),}
        