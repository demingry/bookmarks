from django import forms
from django.contrib.auth.models import User

from account.models import Profile


class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password=forms.CharField(label='Password',widget=forms.PasswordInput)
    repassword=forms.CharField(label='Repeat password',widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=('username','email',)

    def clean_repassword(self):
        cd=self.cleaned_data
        if cd['password'] != cd['repassword']:
            raise forms.ValidationError('Password don\'t match.')
        return cd['repassword']

    def validate(self):
        cd=self.cleaned_data
        return User.objects.filter(username=cd['username']) and User.objects.filter(email=cd['email'])

class UserEditForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('first_name','last_name',)

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=('date_of_birth','photo')
