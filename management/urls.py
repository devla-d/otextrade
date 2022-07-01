from django.urls import path

from .  import views

urlpatterns = [
    path('',views.index,name="managementindex"),
    path('users/',views.users,name="musers"),
    path('users/<int:pk>/',views.usersDetail,name="usersDetail"),

    path('fund-user/',views.fund_user,name="mdeposit"),
    path('withdraw-fund/',views.withdraw_funds,name="mwithdrawal"),

    path('withdrawals/',views.withdrawals,name="withdrawals"),
    path('approve-withdrawal/<int:pk>/',views.approve_withdrawals,name="approve_withdrawals"),
    path('decline-withdrawal/<int:pk>/',views.decline_withdrawals,name="decline_withdrawals"),


    path('deposits/',views.deposits,name="deposits"),

    path('magents/',views.agents,name="magents"),

    path('new-agent/',views.newagents,name="newagents"),

]