from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta,datetime
from countryinfo import CountryInfo
#from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_str
from django.core.mail import EmailMessage
from django.template.loader import get_template


from otex import utils
from users.models import LoginHistory

from .forms import RegisterForm,LoginForm

def sign_out(request):
    logout(request)
    return redirect('sign-in')



def sign_in(request):
    destination = utils.get_next_destination(request)
    request.session['acc_mode'] = "demo"
    browser_type = request.user_agent.browser.family
    browser_version = request.user_agent.browser.version_string
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['email'],password=form.cleaned_data['password'])
            if user:
                login(request,user)
                LoginHistory.objects.create(user=user,ip_add=utils.get_client_ip(request),browser=f"{browser_type} {browser_version}")
                if destination:
                    return redirect(f'{destination}') 
                else:
                    return redirect('trade')
                # return redirect('dashboard')
        else:
            messages.warning(request, ('Invalid Email Or Password.'))
            return redirect('sign-in')
    else:
        form   = LoginForm()
    return render(request,'auth/signin.html',{'form':form})






def sign_up(request):
    
    if request.POST:
        
        email = request.POST.get('email')
        #print(utils.validate_email(email))
        if utils.validate_email(email) == None:
            email_encode  =    urlsafe_base64_encode(force_bytes(email))
            print(email_encode,email)

            current_site = get_current_site(request)
            subject = 'OTEX -- Email verification'
            context = {
                        'email': email_encode,
                        'domain': current_site.domain,
                }
            message = get_template("auth/email_verify.html").render(context)
            mail = EmailMessage(
                subject=subject,
                body=message,
                from_email=utils.EMAIL_ADMIN,
                to=[email],
                reply_to=[utils.EMAIL_ADMIN],
            )
            mail.content_subtype = "html"
            mail.send(fail_silently=True)

            messages.success(request,("Verify Your Email Address"))
            return redirect('sign-up')
        elif utils.validate_email(email) != None:
            messages.warning(request,("This Email Address Is Already In Use"))
            return redirect('sign-up')
        else:
            messages.info(request,("UNKNOWN ERROR OCCOURED"))
            return redirect('sign-up')


    return render(request,'auth/signup.html')


def create_account(request):

    try:
        email = force_str(urlsafe_base64_decode(request.GET.get("trml")))
    except:
        email = None

    if email is not None and utils.validate_email(email) is None:
        if request.POST:
            form= RegisterForm(request.POST)
            if form.is_valid():
                
                instance = form.save(commit=False)
                currencies = CountryInfo(instance.country_of_residence).currencies()
                instance.username = utils.user_unique_id()
                instance.local_currency = currencies[0]
                instance.save()
                messages.success(request,("ACCOUNT CREATED SUCCESSFULLY PLEASE LOGIN"))
                return redirect('sign-in')
            else:

                print(form.errors)
                messages.warning(request,("ERROR"))
                return redirect('sign-in')
        

        else:
            form = RegisterForm(initial={'email':email})
            
        return render(request,'auth/createacc.html',{'form':form})

    else:
        messages.info(request,("UNKNOWN ERROR OCCOURED"))
        return redirect('sign-up')




        
