from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic.base import View

from account.forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from account.models import Profile


@login_required
def dashboard(request):
    return render(request,'account/dashboard.html',{'section':'dashboard','request':request})


def user_login(request):
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    status='successfully'
                else:
                    status='disabled'
            else:
                status='incorrected'
    else:
        status=None
        form=LoginForm()
    return render(request,'account/login.html',{'form':form,'status':status})

def register(request):
    if request.method=='POST':
        user_form=UserRegistrationForm(request.POST)
        if user_form.is_valid():
                new_user=user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password'])
                new_user.save()
                Profile.objects.create(user=new_user)
                return render(request,'account/register_done.html',{'new_user':new_user,})
        else:
            if UserRegistrationForm.validate:
                message='invalid username or email please try again!'
            else:
                message='unstable server'
            user_form = UserRegistrationForm()
            return render(request,'account/register.html',{'message':message,'user_form':user_form})
    else:
        user_form=UserRegistrationForm()
        return render(request,'account/register.html',{'user_form':user_form})

def edit(request):
    if request.method=='POST':
        user_form=UserEditForm(instance=request.user,data=request.POST)
        profile_form=ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Profile updated successfully!')
        else:
            messages.error(request,'Error updating your profile')
    else:
        user_form=UserEditForm(instance=request.user)
        profile_form=ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html',{'user_form': user_form, 'profilre_form': profile_form})
