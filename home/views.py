from django.shortcuts import render
from django.http import JsonResponse



def index(request):
    return render(request,'home/index.html')


def about(request):
    return render(request,'home/about.html')


def careers(request):
    return render(request,'home/careers.html')


def contact(request):
    return render(request,'home/contact.html')



def education(request):
    return render(request,'home/education.html')



def helpcenter(request):
    return render(request,'home/help-center.html')



def customer(request):
    return render(request,'home/customers.html')



def roadmap(request):
    return render(request,'home/roadmap.html')




def legaldocs(request):
    return render(request,'home/legal-docs.html')