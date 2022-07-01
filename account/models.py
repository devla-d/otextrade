from django.db import models
from django.contrib.auth.models import AbstractUser







class Account(AbstractUser):
    email       = models.EmailField(verbose_name='email', max_length=60, unique=True )

    demo_balance         =    models.IntegerField(default=10000)
    balance              =    models.FloatField(default=0)

    

    username            =    models.CharField(max_length=10,unique=True,blank=True,null=True)
    total_deposit        =    models.FloatField(default=0,blank=True,null=True)
    total_withdraw       =    models.FloatField(default=0,blank=True,null=True)



    zipcode                           = models.CharField(max_length=20,blank=True,null=True)
    country_of_residence              = models.CharField(max_length=100,blank=True,null=True)
    citizenship                       = models.CharField(max_length=100,blank=True,null=True)
    place_of_birth                    = models.CharField(max_length=100,blank=True,null=True)


    title              = models.CharField(max_length=100,blank=True,null=True)



    first_address              = models.CharField(max_length=1000,blank=True,null=True)
    second_address              = models.CharField(max_length=1000,blank=True,null=True)
    gender               = models.CharField(max_length=50,blank=True,null=True)

    city                 = models.CharField(max_length=100,blank=True,null=True)
    state                = models.CharField(max_length=100,blank=True,null=True)

    date_of_birth        = models.CharField(max_length=100,blank=True,null=True)

    phone                = models.CharField(max_length=30, blank=True,null=True,unique=True)

    local_currency                = models.CharField(max_length=30, blank=True,null=True,unique=True)



    account_opening_reason                    = models.CharField(max_length=100,blank=True,null=True)


    is_agent                      = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']



    def __str__(self):
        return self.email