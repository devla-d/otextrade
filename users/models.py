from django.db import models


from django.contrib.auth import get_user_model
 
User = get_user_model()

class LoginHistory(models.Model):
    user           = models.ForeignKey(User,on_delete=models.CASCADE)
    ip_add         = models.CharField(max_length=20)
    date           = models.DateTimeField(auto_now_add=True)
    browser        = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} {self.ip_add}"


class BankDetails(models.Model):
    acc_name       = models.CharField(max_length=100)
    acc_number     = models.CharField(max_length=20)
    bank_type      = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.acc_name}"



class Transaction(models.Model):
    user           = models.ForeignKey(User,on_delete=models.CASCADE)
    date           = models.DateTimeField(auto_now_add=True)
    tr_ref         = models.CharField(max_length=20)
    tr_type        = models.CharField(max_length=20)
    amount         = models.FloatField(default=0)
    status         = models.CharField(max_length=20)
    bank_detail    = models.ForeignKey(BankDetails,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f"{self.user.username} -- {self.amount}"



class Contract(models.Model):
    user                 =      models.ForeignKey(User,on_delete=models.CASCADE)
    ty_pe               = models.CharField(max_length=100)
    ty_pe_sub               = models.CharField(max_length=100, default=1)
    date                = models.DateTimeField(auto_now_add=True)
    tr_ref              = models.CharField(max_length=20)
    sell_date          = models.DateTimeField()
    sysmbol             = models.CharField(max_length=100)
    duration_unit      = models.CharField(max_length=100,null=True,blank=True)
    duration            = models.CharField(max_length=100)
    barrier             = models.CharField(max_length=100)
    barrier_sec             = models.CharField(max_length=100,null=True,blank=True)
    stake               =  models.FloatField(default=0)
    payout               =  models.FloatField(default=0)
    payout_total               =  models.FloatField(default=0)
    stake_mode   =    models.CharField(max_length=100,null=True,blank=True)
    status             = models.CharField(max_length=100,null=True,blank=True,default="pending")



    def __str__(self):
        return f"{self.sell_date}"



