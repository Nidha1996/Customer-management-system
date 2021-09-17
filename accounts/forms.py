from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import fields
from django.forms import widgets
from accounts.models import *

class CustomerForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields="__all__"
        exclude=['user']

        # widgets={
        #     'name':forms.TextInput(attrs={'class':'form-control'}),
        #     'phone':forms.TextInput(attrs={'class':'form-control'}),
        #     'email':forms.TextInput(attrs={'class':'form-control'}),
        # }

class Productform(forms.ModelForm):
    class Meta:
        model=Product
        fields="__all__"

        # widgets={
        #     'name':forms.TextInput(attrs={'class':'form-control'}),
        #     'price':forms.TextInput(attrs={'class':'form-control'}),
        #     'category':forms.Select(attrs={'class':'form-control'}),
        #     'description':forms.TextInput(attrs={'class':'form-control'}),
        # }

class Orderform(forms.ModelForm):
    class Meta:
        model=Order
        fields="__all__"

        # widgets={
        #     'customer':forms.Select(attrs={'class':'form-control'}),
        #     'product':forms.Select(attrs={'class':'form-control'}),
        #     'status':forms.Select(attrs={'class':'form-control'}),
        # }

class CreateUserForm(UserCreationForm):
    class Meta:
        model =User
        fields=['username','email','password1','password2']