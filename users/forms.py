from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.utils.safestring import mark_safe

# registation form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    terms_accepted = forms.BooleanField(
        required=True,  # Terms and conditons (didnt set up properly)
        label=mark_safe('I have read and agree to the <a href="/terms/">Terms of Service</a> and <a href="/privacy/">Privacy Policy</a>.')
    )
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)
# Profile registraion form
class ProfileRegisterForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address_line_1', 'address_line_2', 'city', 'postcode', 'country', 'bank_details_placeholder']
        help_texts = {
            'bank_details_placeholder': 'Placeholder only - Do not enter real bank details.',
        }
# User update form
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
# Profile editing
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'address_line_1', 'address_line_2', 'city', 'postcode', 'country', 'bank_details_placeholder']
        help_texts = {
            'bank_details_placeholder': 'Placeholder only - Do not enter real bank details.',
        }
