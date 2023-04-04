from django.db import models
from accounts.models import User


class Benefactor(models.Model):

    EXPERIENCE_CHOICES = [ (0 , "Zero") , (1 , "One") , (2 , "Two")]
    user = models.OneToOneField(User)
    experience = models.SmallIntegerField(choices= EXPERIENCE_CHOICES , default= 0 )
    free_time_per_week = models.PositiveSmallIntegerField(default = 0 )

class Charity(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=50)
    reg_number = models.CharField(max_length=10)


class Task(models.Model):
    GENDER_CHOICES = [ ("M" , "Male") , ("F" , "Female")]
    STATE_CHOICES = [("P" , "Pending") , ("W" "Waiting") , ("A" , "Assigned") , ("D" , "Done")]
    assigned_benifactor  = models.ForeignKey(Benefactor , null=True , on_delete= models.SET_NULL)
    charity = models.ForeignKey(Charity)
    age_limit_from = models.IntegerField(blank = True , null=True)
    age_limit_to = models.IntegerField(blank = True , null =True)
    date = models.DateField(blank = True , null = True)
    description = models.TextField(blank = True , null = True)
    gender_limit = models.CharField(max_length = 1 , choices= GENDER_CHOICES , blank= True , null=True)
    state = models.CharField(default = "P" , choices=STATE_CHOICES)
    title = models.CharField(max_length = 60) 


    
