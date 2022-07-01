from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()








class Agent(models.Model):
    users = models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_agent',blank=True,null=True)
    name = models.CharField(max_length=200)
    min_amount  = models.IntegerField(default=5)
    max_amount  = models.IntegerField(default=2000)
    website     = models.CharField(max_length=1000)
    email       = models.EmailField(verbose_name="Email",max_length=100,blank=True,null=True)
    tel         = models.CharField(max_length=50)
    further_information         = models.TextField(blank=True,null=True)



    def __str__(self):
        return self.user.username