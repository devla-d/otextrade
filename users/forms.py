from django import forms
from django.contrib.auth import get_user_model
 
from otex import utils
User = get_user_model()



class ProfileForm(forms.ModelForm):
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
                'type': 'email',
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
        label = 'First Line of address',
        required=True
    )


    second_address = forms.CharField(   max_length=1000,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'uk-input uk-border-rounded',
                 'placeholder' : 'Second Line of address'
                
            }
        ),
        label = 'Second Line of address',
        required=False
    )





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




    class Meta:
        model = User
        fields = ['first_name','last_name','email','zipcode','first_address','second_address','city','state','date_of_birth','phone','account_opening_reason','title','country_of_residence','citizenship']






 




class PasswordChangeForm(forms.ModelForm):
    user_id = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'hidden',
                'class': 'form-control',

            }
        ),
        label = "",
         required=True
    )
    oldpassword = forms.CharField( max_length=30, label='Old password', widget=forms.PasswordInput(attrs={'placeholder': "OLD PASSWORD", 'class': 'uk-input',}))
    password1 = forms.CharField( max_length=30, label='New Password', widget=forms.PasswordInput(attrs={'placeholder': "NEW PASSWORD", 'class': 'uk-input',}))
    password2 = forms.CharField( max_length=30, label='New password confirmation', widget=forms.PasswordInput(attrs={'placeholder': "New password confirmation", 'class': 'uk-input',}))

    class Meta:
        model = User
        fields = ['user_id','oldpassword','password1','password2']

    def clean(self):
        if self.is_valid():
            user_id = int(self.cleaned_data['user_id'])
            oldpassword = self.cleaned_data['oldpassword']
            password1 =  self.cleaned_data['password1']
            password2 =  self.cleaned_data['password2']
            try:
                user = User.objects.get(id=user_id)
            except:
                user = None
            if user:
                if password1 != password2:
                    raise forms.ValidationError("Passwords don\'t match")
                if not user.check_password(oldpassword):
                    raise forms.ValidationError("Old password don\'t match")
            else:
                raise forms.ValidationError("User dont match")


    def save(self, commit=True):
        user_id = int(self.cleaned_data['user_id'])
        user = User.objects.get(id=user_id)
        password = self.cleaned_data["password1"]
        user.set_password(password)
        if commit:
            user.save()
        return user




