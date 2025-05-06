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

# User registration view
def register(request):
    if request.method == 'POST': # Load data into both forms
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileRegisterForm(request.POST) 

        if user_form.is_valid() and profile_form.is_valid(): #Validate forms
            user = user_form.save() #saves user
            profile_instance_form = ProfileRegisterForm(request.POST, instance=user.profile)
            if profile_instance_form.is_valid():
                 profile_instance_form.save() 
            else:
                 messages.error(request, 'An unexpected error occurred updating profile details. Please contact support.')
                 context = {
                    'user_form': user_form, 
                    'profile_form': profile_form, 
                    'title': 'Registration'
                 }
                 return render(request, 'users/register.html', context)


            username = user_form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login') # Redirect to llogin
        else:

            messages.error(request, 'Registration failed. Please correct the errors below.') 

    else:
        #sshow empty forms
        user_form = UserRegisterForm()
        profile_form = ProfileRegisterForm()
        
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Registration'
    }
    return render(request, 'users/register.html', context)

# Profile View 
@login_required
def profile(request):
    if request.method == 'POST': #load updated data
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES, 
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile') # Redirect back to profile page if all good
        else:
             messages.error(request, 'Please correct the errors below.')

    else: #show values
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'Profile'
    }
    return render(request, 'users/profile.html', context)


