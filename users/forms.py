from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.utils.safestring import mark_safe


class UserRegisterForm(UserCreationForm):
    # email field definition is inherited or can be added if customization needed
    email = forms.EmailField(required=True)
    # RESTORE terms_accepted field
    terms_accepted = forms.BooleanField(
        required=True, 
        label=mark_safe('I have read and agree to the <a href="/terms/">Terms of Service</a> and <a href="/privacy/">Privacy Policy</a>.')
    )
    
    class Meta(UserCreationForm.Meta):
        model = User
        # Fields handled by UserCreationForm: username, password, password_confirmation
        # Add email here
        fields = UserCreationForm.Meta.fields + ('email',)



# New form for Profile fields during registration
class ProfileRegisterForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address_line_1', 'address_line_2', 'city', 'postcode', 'country', 'bank_details_placeholder']
        # Add help text for the placeholder
        help_texts = {
            'bank_details_placeholder': 'Placeholder only - Do not enter real bank details.',
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'address_line_1', 'address_line_2', 'city', 'postcode', 'country', 'bank_details_placeholder']
        # Add help text for the placeholder
        help_texts = {
            'bank_details_placeholder': 'Placeholder only - Do not enter real bank details.',
        }
