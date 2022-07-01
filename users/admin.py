from django.contrib import admin

from .models import LoginHistory,Transaction,BankDetails,Contract

admin.site.register(LoginHistory)
admin.site.register(Transaction)
admin.site.register(BankDetails)
admin.site.register(Contract)