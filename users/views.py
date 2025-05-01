from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import logout
# Update form imports
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProfileRegisterForm 
from .models import Profile # Import Profile model

# Create your views here.

# Registration View - Restore correct two-form handling
def register(request):
    if request.method == 'POST':
        # Use correct variable names
        user_form = UserRegisterForm(request.POST)
        # Profile form needs to be handled differently now
        # profile_form = ProfileRegisterForm(request.POST)
        
        # Check validity of ONLY the user_form first
        if user_form.is_valid():
            user = user_form.save() # Save the User object - this triggers the create_profile signal
            
            # Now bind the profile form data to the EXISTING profile instance created by the signal
            profile_form = ProfileRegisterForm(request.POST, instance=user.profile)

            # Validate and save the profile form to update the details
            if profile_form.is_valid():
                profile_form.save() # Saves the updates to user.profile
                
                username = user_form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}! You can now log in.')
                return redirect('login') # Redirect using the name from Tapps/urls.py
            else:
                # Profile form is invalid, errors should be shown
                messages.error(request, 'Registration failed. Please correct the profile details below.') 
                # Note: The user object was created, but profile update failed. 
                # You might want to handle this case differently (e.g., delete the user or guide them to profile page)
                # For now, we re-render the form with errors.
        else:
            # User form is invalid, instantiate profile_form without instance for re-rendering
            profile_form = ProfileRegisterForm(request.POST)
            messages.error(request, 'Registration failed. Please correct the user details below.') 
    else:
        # For GET requests, instantiate blank forms
        user_form = UserRegisterForm()
        profile_form = ProfileRegisterForm()
        
    # Pass both forms to the template context with correct names
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Registration'
    }
    return render(request, 'users/register.html', context)

# Profile View - Handle two forms
@login_required
def profile(request):
    if request.method == 'POST':
        # Pass instance=request.user for User form
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # Pass instance=request.user.profile for Profile form
        # Also pass request.FILES for image upload
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES, 
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile') # Redirect back to profile page
        else:
             messages.error(request, 'Please correct the errors below.')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'Profile'
    }
    return render(request, 'users/profile.html', context)

# Account Deletion View
class AccountDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('techmarket:home') # Redirect to home page after deletion
    # Ensure the user being deleted is the logged-in user
    def test_func(self):
        return self.request.user == self.get_object()
    #Get the object to be deleted (the logged-in user)
    def get_object(self, queryset=None):
        return self.request.user

    #Add success message after deletion
    def form_valid(self, form):
        user = self.get_object()
        logout(self.request) #Logout the user out before deleting
        messages.success(self.request, f'Account for {user.username} has been successfully deleted.')
        return super().form_valid(form)
