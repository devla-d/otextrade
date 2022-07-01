from sys import prefix
from django.shortcuts import render,redirect,get_object_or_404
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site

from countryinfo import CountryInfo
from .decorator import manager_required
from django.contrib.auth import get_user_model
 
User = get_user_model()

from otex import utils
from users.models import  Transaction
from .models import Agent
from .forms import NewaForm,NewAgentForm


@manager_required
def index(request):
    am_deposit = 0
    am_withdraw = 0
    for obj in Transaction.objects.all():
        if obj.tr_type == utils.D:
            am_deposit += obj.amount
        elif obj.tr_type == utils.W:
            am_withdraw += obj.amount

    context = {
       
        'am_deposit' : am_deposit,
        'am_withdraw': am_withdraw,
        'users':User.objects.all().count(),
         
        'transactions':Transaction.objects.all().count(),
       
    }
    return render(request,'management/index.html',context)


@manager_required
def withdrawals(request):
    context = {
       
        'transactions' : Transaction.objects.filter(tr_type = utils.W).order_by('-date'),
        
       
    }
    return render(request,'management/withdrawals.html',context)


@manager_required
def deposits(request):
    context = {
       
        'transactions' : Transaction.objects.filter(tr_type = utils.D).order_by('-date'),
        
       
    }
    return render(request,'management/deposits.html',context)






@manager_required
def users(request):
    context = {
       
        'users' : User.objects.all(),
        
       
    }
    return render(request,'management/users.html',context)



@manager_required
def usersDetail(request,pk):
    account = get_object_or_404(User,pk=pk)
    return render(request,'management/users_detail.html',{'account':account})




@manager_required
def fund_user(request):
    if request.POST:
        pk = int(request.POST.get('account_id'))
        amount = float(request.POST.get('amount')) 
        acc   =  get_object_or_404(User,pk=pk)


        transaction = Transaction.objects.create(user=acc,tr_ref=utils.transactioncode(),
                                                    tr_type=utils.D,
                                                    amount=amount,status=utils.SUC)
        acc.balance += amount
        acc.total_deposit += amount
        acc.save()




        current_site = get_current_site(request)
        subject = 'Account Deposited'
        context = {
            'user': acc,
            'domain': current_site.domain,
            'amount': amount,
            'transaction':transaction

            }
        message = get_template("management/deposit_email.html").render(context)
        mail = EmailMessage(
            subject=subject,
            body=message,
            from_email=utils.EMAIL_ADMIN,
            to=[acc.email],
            reply_to=[utils.EMAIL_ADMIN],
        )
        mail.content_subtype = "html"
        mail.send(fail_silently=True)



        messages.success(request,'Account Deposit Successful')
        return redirect('usersDetail',pk=acc.id)

    messages.warning(request,'UKNOWN ERROR OCCURED')
    return redirect('musers')




@manager_required
def withdraw_funds(request):
    if request.POST:
        pk = int(request.POST.get('account_id'))
        amount = float(request.POST.get('amount')) 
        acc   =  get_object_or_404(User,pk=pk)

        if acc.balance >= amount:


            transaction = Transaction.objects.create(user=acc,tr_ref=utils.transactioncode(),
                                                        tr_type=utils.W,
                                                        amount=amount,status=utils.SUC)
                
            acc.balance -= amount
            acc.total_withdraw += amount
            acc.save()




            current_site = get_current_site(request)
            subject = f'[{acc.username}] - Withdrawal Successful'
            context = {
                'user': acc,
                'domain': current_site.domain,
                'amount': amount,
                'transaction':transaction

                }
            message = get_template("management/with_email.html").render(context)
            mail = EmailMessage(
                subject=subject,
                body=message,
                from_email=utils.EMAIL_ADMIN,
                to=[acc.email],
                reply_to=[utils.EMAIL_ADMIN],
            )
            mail.content_subtype = "html"
            mail.send(fail_silently=True)



            messages.success(request,'Account Withdrawal Successful')
            return redirect('usersDetail',pk=acc.id)

        messages.warning(request,'Insufficent Funds')
        return redirect('usersDetail',pk=acc.id)

    messages.warning(request,'UKNOWN ERROR OCCURED')
    return redirect('musers')



@manager_required
def approve_withdrawals(request,pk):
    withdrawal = get_object_or_404(Transaction,pk=pk)
    withdrawal.status = utils.SUC
    withdrawal.save()



    current_site = get_current_site(request)
    subject = f'[{withdrawal.user.username}] - Withdrawal Approved'
    context = {
        'user': withdrawal.user,
        'domain': current_site.domain,
        'amount': withdrawal.amount,
        'transaction':withdrawal,
        'status' : 'approved'

        }
    message = get_template("management/proc_with_email.html").render(context)
    mail = EmailMessage(
        subject=subject,
        body=message,
        from_email=utils.EMAIL_ADMIN,
        to=[withdrawal.user.email],
        reply_to=[utils.EMAIL_ADMIN],
    )
    mail.content_subtype = "html"
    mail.send(fail_silently=True)


    messages.success(request,'Withdrawal Approved')
    return redirect('withdrawals')








@manager_required
def decline_withdrawals(request,pk):
    withdrawal = get_object_or_404(Transaction,pk=pk)
    withdrawal.status = utils.DEC
    withdrawal.save()



    current_site = get_current_site(request)
    subject = f'[{withdrawal.user.username}] - Withdrawal Declined'
    context = {
        'user': withdrawal.user,
        'domain': current_site.domain,
        'amount': withdrawal.amount,
        'transaction':withdrawal,
        'status' : 'declined'

        }
    message = get_template("management/proc_with_email.html").render(context)
    mail = EmailMessage(
        subject=subject,
        body=message,
        from_email=utils.EMAIL_ADMIN,
        to=[withdrawal.user.email],
        reply_to=[utils.EMAIL_ADMIN],
    )
    mail.content_subtype = "html"
    mail.send(fail_silently=True)


    messages.warning(request,'Withdrawal Declined')
    return redirect('withdrawals')










@manager_required
def agents(request):
    agents = Agent.objects.all()
    return render(request,'management/agents.html',{'agents':agents})




@manager_required
def newagents(request):
    if request.POST:
        form_1 = NewAgentForm(request.POST,prefix="form_1")
        form_2 = NewaForm(request.POST,prefix="form_2")

        if form_1.is_valid() and form_2.is_valid():
            agent = form_1.save(commit=False)
            account = form_2.save(commit=False)
            currencies = CountryInfo(account.country_of_residence).currencies()

            account.is_agent = True
            account.username  = utils.user_unique_id()
            account.local_currency = currencies[0]
            account.save()
            agent.user = account
            agent.save()

            messages.success(request,"Agent account created successfuly")
            return redirect('magents')

    else:
        form_1 = NewAgentForm(prefix="form_1")
        form_2 = NewaForm(prefix="form_2")
    return render(request,'management/newagent.html',{'form_1':form_1,"form_2":form_2})