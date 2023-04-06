from django.shortcuts import render
from accounts.models import User

# Create your views here.

def about_us(request):
    # View for about-us page
    user_queryset = User.objects.all()
    full_name_list = []
    for user in user_queryset:
        full_name_list.append(user.get_full_name())

    return render(request , "about_us.html" , context = {"full_name_list" : full_name_list})


