from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User


class registreform(UserCreationForm):
    class Meta:
        model=User
        fields=('username','email','password1','password2')
        widgets={
            'username':forms.TextInput(attrs={'class':'w-full border-b-2 m-2 p-2 border-black rounded-md focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50'}),
            'email' :forms.EmailInput(attrs={'class':'w-full border-b-2 m-2 p-2 border-black rounded-md focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50'}),
            'password1' :forms.PasswordInput(attrs={'class':'w-full border-b-2 m-2 p-2 border-black rounded-md focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50'}),
            'password2' :forms.PasswordInput(attrs={'class':'w-full border-b-2 m-2 p-2 border-black rounded-md focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50'})
        }
