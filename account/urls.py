from django.urls import path
from . import views

from django.contrib.auth import  views as auth_view


urlpatterns = [

    path('sign-in/',views.sign_in,name='sign-in'),
    path('sign-up/',views.sign_up,name='sign-up'),

    path('sign-out/',views.sign_out,name='sign-out'),

    path('new-account/',views.create_account,name='create_account'),






    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='auth/password-reset.html'), name='password-reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='auth/password-reset-done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_view.PasswordResetConfirmView.as_view(template_name='auth/password-reset-confirm.html'), name='password_reset_confirm'),
    path('password-reset/complete/', auth_view.PasswordResetCompleteView.as_view(template_name='auth/password-reset-complete.html'), name='password_reset_complete'),
    
]