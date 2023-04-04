from django.db import models
from accounts.models import User


class Benefactor(models.Model):

    EXPERIENCE_CHOICES = [ 0 , 1 , 2]
    user = models.OneToOneField(User)
    experience = models.SmallIntegerField(choices= EXPERIENCE_CHOICES , default= 0 )
    free_time_per_week = models.PositiveSmallIntegerField(default = 0 )


    


class Charity(models.Model):
    pass


class Task(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=50)
    reg_number = models.CharField(max_length=10)
    
