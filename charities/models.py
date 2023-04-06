from django.db import models
from accounts.models import User
from itertools import chain


class Benefactor(models.Model):

    EXPERIENCE_CHOICES = [ (0 , "Zero") , (1 , "One") , (2 , "Two")]
    user = models.OneToOneField(User , on_delete= models.CASCADE)
    experience = models.SmallIntegerField(choices= EXPERIENCE_CHOICES , default= 0 )
    free_time_per_week = models.PositiveSmallIntegerField(default = 0 )

class Charity(models.Model):
    user = models.OneToOneField(User , on_delete= models.CASCADE)
    name = models.CharField(max_length=50)
    reg_number = models.CharField(max_length=10)


class TaskManager(models.Manager):
    def related_tasks_to_charity(self, user):
        users_charity = user.charity   #model_lowercased name
        if users_charity == None:
            return self.none() 
        else:
            result = self.filter(charity = users_charity)
            return result

    def related_tasks_to_benefactor(self, user):
        users_benefactor = user.benefactor
        if users_benefactor == None:
            return self.none()
        else:
            result = self.filter(assigned_benefactor = users_benefactor)
            return result

    def all_related_tasks_to_user(self, user):
        if user.charity == None:
            users_charity_tasks = self.none()
        else:
            users_charity_tasks  = self.filter(charity = user.charity)
        if user.benefactor == None:
            users_benefactor_tasks = self.none()
        else:
            users_benefactor_tasks = self.filter(assigned_benefactor = user.benefactor)
        pending_tasks = self.filter(state = "P")
        return users_benefactor_tasks + users_charity_tasks + pending_tasks


class Task(models.Model):
    GENDER_CHOICES = [ ("M" , "Male") , ("F" , "Female")]
    STATE_CHOICES = [("P" , "Pending") , ("W" , "Waiting") , ("A" , "Assigned") , ("D" , "Done")]
    assigned_benefactor  = models.ForeignKey(Benefactor , null=True , on_delete= models.SET_NULL)
    charity = models.ForeignKey(Charity , on_delete= models.CASCADE)
    age_limit_from = models.IntegerField(blank = True , null=True)
    age_limit_to = models.IntegerField(blank = True , null =True)
    date = models.DateField(blank = True , null = True)
    description = models.TextField(blank = True , null = True)
    gender_limit = models.CharField(max_length = 1 , choices= GENDER_CHOICES , blank= True , null=True)
    state = models.CharField(default = "P" , choices=STATE_CHOICES , max_length=1)
    title = models.CharField(max_length = 60) 
    objects = TaskManager()

    
