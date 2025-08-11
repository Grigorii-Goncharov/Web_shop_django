# forms.py
from django import forms
from .models import Products

class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'description', 'image', 'category', 'purchase_price' ]