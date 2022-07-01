from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
# from django.utils.encoding import force_str
# from django.core.mail import EmailMessage
# from django.template.loader import get_template

import requests
from management.models import Agent
from otex import utils
from .models import LoginHistory,BankDetails,Transaction,Contract
from . forms import ProfileForm

@login_required
def trade(request):
    mode = request.session.get('acc_mode')
    return render(request,'users/trade.html',{"mode":mode})


@csrf_exempt
def create_contract(request):
    user = request.user
    context = {}
    mode = request.session.get('acc_mode')


    symbol = request.POST.get('symbol')
    stake_type = request.POST.get('stake_type')
    duration = request.POST.get('duration')
    duration_unit = request.POST.get('duration_unit')
    barrier = request.POST.get('barier')
    stakeamount = int(request.POST.get('stakeamount'))
    payout = request.POST.get('payout')
    payout_total = request.POST.get('payout_total')
    ty_pe = request.POST.get('ty_pe')

    if duration_unit == "t":
        sell_date_ = timezone.now()
    else:
        if duration_unit == 'h':
            sell_date_ = utils.get_deadline(int(duration),0,0)
        if duration_unit == 'm':
            unit = "minutes"
            sell_date_ = utils.get_deadline(0,int(duration),0)
        if duration_unit == 'd':
            unit = "days"
            sell_date_ = utils.get_deadline(0,0,int(duration))

        


    if mode == 'demo' and user.demo_balance >= stakeamount:
        contract = Contract.objects.create(
                 user=user,ty_pe=ty_pe,ty_pe_sub=stake_type,
                 tr_ref=utils.transactioncode(),sell_date=sell_date_,sysmbol=symbol,
                 duration_unit=duration_unit,duration=duration,barrier=barrier,stake=stakeamount,
                 payout = payout,payout_total=payout_total,stake_mode=mode

             )
        user.demo_balance -= stakeamount
        user.save()
        context['tr_ref'] = contract.tr_ref
        return JsonResponse(context)
    
    elif mode == 'real' and user.balance >= stakeamount:
        contract = Contract.objects.create(
                 user=user,ty_pe=ty_pe,ty_pe_sub=stake_type,
                 tr_ref=utils.transactioncode(),sell_date=sell_date_,sysmbol=symbol,
                 duration_unit=duration_unit,duration=duration,barrier=barrier,stake=stakeamount,
                 payout = payout,payout_total=payout_total,stake_mode=mode

             )
        user.balance -= stakeamount
        user.save()
        context['tr_ref'] = contract.tr_ref
        return JsonResponse(context)

    else:
        context['err'] = "Insuficcient Funds"
        return JsonResponse(context)
        





@csrf_exempt
@login_required
def check_trade(request,tr_ref):
    contract = get_object_or_404(Contract,tr_ref=tr_ref)
    user = request.user
    context = {}
    if request.POST:
        barier = request.POST.get('barier')
        print(barier)
        if contract.ty_pe == "Higher":
            if barier > contract.barrier:
                contract.status = 'gain'
                if contract.stake_mode == 'demo':
                    user.demo_balance += contract.payout_total
                else:
                    user.balance += contract.payout_total
                user.save()
                contract.save()
                context['msg'] = 'Trade Won'
                return JsonResponse(context)
            else:
                contract.status = 'loss'
                contract.save()
                context['msg'] = 'Trade loss'
                return JsonResponse(context)

        if contract.ty_pe == "Lower":
            if barier < contract.barrier:
                contract.status = 'gain'
                if contract.stake_mode == 'demo':
                    user.demo_balance += contract.payout_total
                else:
                    user.balance += contract.payout_total
                user.save()
                contract.save()
                context['msg'] = 'Trade won'
                return JsonResponse(context)
            else:
                contract.status = 'loss'
                contract.save()
                context['msg'] = 'Trade loss'
                return JsonResponse(context)



        if contract.ty_pe == "Touch":
            if barier == contract.barrier:
                contract.status = 'gain'
                if contract.stake_mode == 'demo':
                    user.demo_balance += contract.payout_total
                else:
                    user.balance += contract.payout_total
                user.save()
                contract.save()
                context['msg'] = 'Trade won'
                return JsonResponse(context)
            else:
                contract.status = 'loss'
                contract.save()
                context['msg'] = 'Trade loss'
                return JsonResponse(context)




        if contract.ty_pe == "No Touch":
            if barier != contract.barrier:
                contract.status = 'gain'
                if contract.stake_mode == 'demo':
                    user.demo_balance += contract.payout_total
                else:
                    user.balance += contract.payout_total
                user.save()
                contract.save()
                context['msg'] = 'Trade won'
                return JsonResponse(context)
            else:
                contract.status = 'loss'
                contract.save()
                context['msg'] = 'Trade loss'
                return JsonResponse(context)





    return render(request,'users/checktrade.html',{'contract':contract})










@login_required
def reset_demo_balance(request):
    user = request.user
    user.demo_balance = 10000
    user.save()
    messages.success(request,"Balance Reset")
    return redirect('trade')

@login_required
def swith_account(request,tomode):
    request.session['acc_mode'] = tomode


    messages.success(request,"Account Mode Changed")
    return redirect('trade')

@login_required
def profit_table(request):
    contract = Contract.objects.filter(user=request.user)
    return render(request,'users/profit-table.html',{'contract':contract})


@login_required
def cashier(request):
    return render(request,'users/cashier.html')


def agents(request):
    agents = Agent.objects.all()
    return render(request,'users/agents.html',{'agents':agents})

@login_required
def transactions(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request,"users/transactions.html",{'transactions':transactions})



@login_required
def withdrawal(request):
    user = request.user
    if request.POST:
        wbank = request.POST.get('Wbank')
        #print(wbank)
        Waccno = request.POST.get('Waccno')
        Waccname = request.POST.get('Waccname')
        Wamount = float(request.POST.get('Wamount'))
        if user.balance >= Wamount:
            transaction = Transaction.objects.create(user=user,tr_ref=utils.transactioncode(),tr_type=utils.W,amount=Wamount,status=utils.PED)
            bank_detail = BankDetails.objects.create(acc_name=Waccname,acc_number=Waccno,bank_type=wbank)
            transaction.bank_detail = bank_detail
            user.balance -= Wamount
            user.total_withdraw += Wamount
            user.save()
            transaction.save()
            messages.success(request,("Your withdrawal request has been submited"))
            return redirect('withdrawal')
        messages.warning(request,("Insuficient funds"))
        return redirect('withdrawal')
    return render(request,'users/withdrawal.html')



@login_required
def profile(request):
    
    user= request.user
    if request.POST:
        form = ProfileForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,"Account Updated Successfull")
            return redirect('profile')
    else:
        form = ProfileForm(instance=user)
    return render(request,'users/profile.html',{'form':form})




@login_required
def carddeposit(request):
    txRef = utils.tx_ref()
    user = request.user
    
    if request.POST:
        # txRef = request.POST.get('tx_ref')
        # status = request.POST.get('status')
        # charged_amount = request.POST.get('charged_amount')
        print(request.POST.get('amount_in_usd'))
        amount = float(request.POST.get('amount_in_usd'))
        # inittxRef = request.POST.get('inittxRef')

        # if inittxRef == txRef:
        #     if status == "successful":
        #         return JsonResponse({'msg':'Payment successful'})
        #     else:
        #         return JsonResponse({'msg':'Payment error'})
        # else:
        #     return JsonResponse({'msg':'Payment error'})
        
        return redirect(str(process_payment(request,f"{user.first_name} {user.last_name}",user.email,amount,user.phone,txRef)))

                


    return render(request,'users/cardepost.html')


def process_payment(req,name,email,amount,phone,txRef):

    req.session['depo_amount'] = amount
    req.session['tx_ref'] = txRef



    auth_token= "FLWSECK_TEST-a00c6d616ae0b2af3c41303d0897434c-X"
    hed = {'Authorization': 'Bearer ' + auth_token}
    data = {
            "tx_ref":txRef,
            "amount":amount,
            "currency":"USD",
            "redirect_url":"http://127.0.0.1:8000/verify-payments/",
            "payment_options":"card",
            "meta":{
                "consumer_id":23,
                "consumer_mac":"92a3-912ba-1192a"
            },
            "customer":{
                "email":email,
                "phonenumber":phone,
                "name":name
            },
            "customizations":{
                "title": "Otex",
                "description": "Deposit funds",
                "logo": "https://www.logolynx.com/images/logolynx/22/2239ca38f5505fbfce7e55bbc0604386.jpeg",
            }
            }
    url = ' https://api.flutterwave.com/v3/payments'
    response = requests.post(url, json=data, headers=hed)
    response=response.json()
    link=response['data']['link']
    return link






@login_required
def verifycard(request):
    user = request.user
    status=request.GET.get('status', None)
    tx_ref=request.GET.get('tx_ref', None)
    tx_ref_t = request.session.get('tx_ref')
    depo_amount_i  = request.session.get('depo_amount')
    if depo_amount_i is not None:
        depo_amount = float(depo_amount_i)
    context = {}

    

    if tx_ref is not None and tx_ref_t is not None:
        if tx_ref == tx_ref_t:
            del request.session['tx_ref']
            del request.session['depo_amount']
            if status == "successful":
                transactions = Transaction.objects.create(user=user,tr_ref=utils.transactioncode(),
                                                            tr_type=utils.D,
                                                            amount=depo_amount,status=utils.SUC)
                user.balance += depo_amount
                user.total_deposit += depo_amount
                user.save()
                context['msg']  = "successful"
                context['tr_rx']  = transactions.tr
                context['amount']  = transactions.amount
            elif status == 'failed':
                transactions = Transaction.objects.create(user=user,tr_ref=utils.transactioncode(),
                                                            tr_type=utils.D,
                                                            amount=depo_amount,status=utils.DEC)
                context['msg']  = "faild"
                context['tr_rx']  = transactions.tr_ref
                context['amount']  = transactions.amount
            else:
                messages.warning(request,(" Uh-oh. Please try again, or contact support if you're encountering difficulties making payment."))
                return redirect('card-deposit')


            return render(request,'users/verifycard.html',context)

    
    messages.warning(request,("Link Is Invalid."))
    return redirect('card-deposit')

    

    
 







@login_required
def settings(request):
    return render(request,'users/settings.html')







@login_required
def loginhistory(request):
    logs = LoginHistory.objects.filter(user=request.user).order_by('-date')
    return render(request,'users/loginhistory.html',{'logs':logs})



@login_required
def acc_limit(request):
    return render(request,'users/acc_limit.html')






