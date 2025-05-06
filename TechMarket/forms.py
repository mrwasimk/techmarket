from django import forms
from django.core.validators import EmailValidator
from .models import Product

#Contact form
class Contact(forms.Form):
    Firstname = forms.CharField(max_length=50)
    Surename = forms.CharField(max_length=50)
    Email = forms.CharField(validators=[EmailValidator()])
    Address = forms.CharField(max_length=50)
    Phonenumber = forms.CharField(max_length=11)
    Message = forms.CharField(widget=forms.Textarea)
# Product form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']
