from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PackageForm(forms.ModelForm):
    class Meta:
        model= Package
        fields='__all__'
        exclude=['date_added','slug']

class RegistrationForm(UserCreationForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter First Name'}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Last Name'}))
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Username'}))
    email=forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Enter email'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
    class Meta:
        model=User
        fields= ['first_name','last_name','username','email','password1','password2']


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['image']


class UserPackageForm(forms.ModelForm):
    class Meta:
        model=UserPackage
        fields='__all__'