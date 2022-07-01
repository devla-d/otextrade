from django.urls import path
from . import views

urlpatterns = [

    path('trade/',views.trade,name='trade'),
    path('reset-balace/',views.reset_demo_balance,name='resetdemobalace'),

    path('change-mode/<str:tomode>/',views.swith_account,name='swith_account'),


    path('profit-table/',views.profit_table,name='profit-table'),
    path('cashier/',views.cashier,name='cashier'),
    path('agents/',views.agents,name='agents'),
    path('card-deposit/',views.carddeposit,name='card-deposit'),
    path('profile/',views.profile,name='profile'),
    path('settings/',views.settings,name='settings'),
    # path('settings/change-password/',views.change_password,name='change-password'),
    # path('settings/change-password/new-password/<str:email>/',views.change_password_reset,name='new-password'),
    
    path('transactions',views.transactions,name="transactions"),
    path('withdrawal',views.withdrawal,name="withdrawal"),

    path('login-history/',views.loginhistory,name='login-history'),

    path('account-limit/',views.acc_limit,name="acc-limit"),

     path('verify-payments/',views.verifycard,name="verify-card"),


     path('create-contract/',views.create_contract,name="create-contract"),


     path('trade/<str:tr_ref>/',views.check_trade,name="check_trade"),


]