from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="home"),
    path('about/',views.about,name="about"),
    path('careers/',views.careers,name="careers"),
    path('contact/',views.contact,name="contact"),
    path('education/',views.education,name="education"),
    path('help-center/',views.helpcenter,name="help-center"),
    path('customers/',views.customer,name="customers"),
    path('roadmap/',views.roadmap,name="roadmap"),
    path('legal-docs/',views.legaldocs,name="legal-docs"),
]