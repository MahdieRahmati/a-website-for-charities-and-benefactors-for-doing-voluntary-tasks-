from django.db import models
from accounts.models import User

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

        if hasattr(user , "charity"):
            users_charity = user.charity
            result = self.filter(charity = users_charity)
            return result
        else:
            return Task.objects.none()


    def related_tasks_to_benefactor(self, user):
        if hasattr(user , "benefactor"):
            users_benefactor = user.benefactor
            result = self.filter(assigned_benefactor = users_benefactor)
            return result
        else:
            return Task.objects.none()


    def all_related_tasks_to_user(self, user):
        users_charity_tasks = self.related_tasks_to_charity(user)
        users_benefactor_tasks = self.related_tasks_to_benefactor(user)
        pending_tasks = self.filter(state = "P")
        return users_benefactor_tasks | users_charity_tasks | pending_tasks


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

    
