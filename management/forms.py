from django import forms
from .models import Agent
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from otex import utils
User = get_user_model()


class NewaForm(UserCreationForm):
    first_name = forms.CharField(   max_length=150,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
               
                'placeholder' : 'First name'
                
            }
        ),
        label = 'First name',
        required=True
    )
    last_name = forms.CharField(   max_length=150,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
               
                 'placeholder' : 'Last Name'
                
            }
        ),
        label = 'Last Name',
        required=True
    )
    email = forms.EmailField(max_length=100)
    username  =  forms.CharField(   max_length=10,
        widget=forms.TextInput(
            attrs={
                'type': 'hidden'
                
            }
        ),
        label = ' ',
        required=False
    )

    country_of_residence = forms.ChoiceField(choices = utils.COUNTRIES)


    password1 = forms.CharField( max_length=10, min_length=6,label='Password', widget=forms.PasswordInput(
            attrs={
                'placeholder': "Password",
               
        }))
    password2 = forms.CharField( max_length=10, min_length=6,label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': "Comfirm Password"}))



    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','country_of_residence','password1','password2']



class NewAgentForm(forms.ModelForm):
    name = forms.CharField(   max_length=150,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
               
                'placeholder' : 'Name You Want On Agent Pages'
                
            }
        ),
        label = 'Nick Name',
        required=True
    )
    class Meta:
        model = Agent
        fields = ['name','website','tel','further_information']
