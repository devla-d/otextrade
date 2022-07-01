from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from otex import utils
User = get_user_model()

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(   max_length=150,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'uk-input uk-border-rounded',
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
                'class': 'uk-input uk-border-rounded',
                 'placeholder' : 'Last Name'
                
            }
        ),
        label = 'Last Name',
        required=True
    )
    email = forms.EmailField(   max_length=80,
        widget=forms.TextInput(
            attrs={
                'type': 'hidden',
                'class': 'uk-input uk-border-rounded',
                'placeholder' : 'Email'
                
            }
        ),
        label = 'Email',
        required=True
    )

    zipcode = forms.CharField(   max_length=50,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'uk-input uk-border-rounded',
                 'placeholder' : 'Zipcode'
                
            }
        ),
        label = 'Zipcode',
        required=True
    )





    first_address = forms.CharField(   max_length=1000,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'uk-input uk-border-rounded',
                 'placeholder' : 'First Line of address'
                
            }
        ),
        label = 'Address',
        required=True
    )


    # second_address = forms.CharField(   max_length=1000,
    #     widget=forms.TextInput(
    #         attrs={
    #             'type': 'text',
    #             'class': 'uk-input uk-border-rounded',
    #              'placeholder' : 'Second Line of address'
                
    #         }
    #     ),
    #     label = 'Second Line of address',
    #     required=False
    # )





    city = forms.CharField(   max_length=1000,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'uk-input uk-border-rounded',
                 'placeholder' : 'City'
                
            }
        ),
        label = 'City',
        required=True
    )





    state = forms.CharField(   max_length=1000,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'uk-input uk-border-rounded',
                 'placeholder' : 'State'
                
            }
        ),
        label = 'State / province',
        required=True
    )



    date_of_birth = forms.CharField(   max_length=1000,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'uk-input uk-border-rounded',
                 'placeholder' : 'Date Of Birth'
                
            }
        ),
        label = 'Date Of Birth',
        required=True
    )





    phone = forms.CharField(   max_length=1000,
        widget=forms.TextInput(
            attrs={
                'type': 'tel',
                'class': 'uk-input uk-border-rounded',
                 'placeholder' : 'Phone'
                
            }
        ),
        label = 'Phone',
        required=True
    )




    account_opening_reason = forms.ChoiceField(choices = utils.ACCOUNTOPR,widget=forms.Select(
        attrs={
            'class':"uk-select"
        }
    ),)

    title = forms.ChoiceField(choices = utils.TITLE, widget=forms.Select(
        attrs={
            'class':"uk-select"
        }
    ),)

    country_of_residence = forms.ChoiceField(choices = utils.COUNTRIES,widget=forms.Select(
        attrs={
            'class':"uk-select"
        }
    ),)

    citizenship = forms.ChoiceField(choices = utils.COUNTRIES,widget=forms.Select(
        attrs={
            'class':"uk-select"
        }
    ),)


    password1 = forms.CharField( max_length=30, min_length=6,label='Password', widget=forms.PasswordInput(
            attrs={
                'placeholder': "Password", 'class': 'uk-input',
                # "pattern" : "(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}",
                # "title":"Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters" 
        }))
    password2 = forms.CharField( max_length=30, min_length=6,label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': "Comfirm Password", 'class': 'uk-input',}))


    username = forms.CharField(   max_length=10,
        widget=forms.TextInput(
            attrs={
                'type': 'hidden'
                
            }
        ),
        label = ' ',
        required=False
    )
    class Meta:
        model = User
        fields = ['first_name','last_name','email','zipcode','first_address','city','state','date_of_birth','phone','account_opening_reason','title','country_of_residence','citizenship','password1','password2']







class LoginForm(forms.ModelForm):
    email = forms.EmailField(   max_length=80,
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'class': 'uk-input uk-border-rounded',
                 'placeholder' : 'Email'
                
            }
        ),
        label = 'Email',
        required=True
    )
    password = forms.CharField( max_length=30, min_length=6,label='Password', widget=forms.PasswordInput(attrs={'placeholder': "Password", 'class':'uk-input uk-border-rounded',}))

    class Meta:
        model = User
        fields = ('email','password')


    def clean(self):
        if self.is_valid():
            if not authenticate(email=self.cleaned_data['email'],password=self.cleaned_data['password']):
                raise forms.ValidationError('Invalid Email and Password')