from django.shortcuts import render
from charities.models import Benefactor

# Create your views here.

def about_us(request):
    # View for about-us page
    benefactor_queryset = Benefactor.objects.all().values_list("user" , flat = True)
    full_name_list = []
    for user in benefactor_queryset:
        full_name_list.append(user.get_full_name())

    return render(request , "about_us.html" , context = {"full_name_list" : full_name_list})


