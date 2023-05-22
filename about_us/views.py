from django.shortcuts import render
from accounts.models import User

from django.contrib.auth import get_user_model
from django.shortcuts import render


def about_us(request):
    context = {
        'members': get_user_model().objects.all()
    }
    return render(request, 'about_us.html', context)

# Create your views here.

# def about_us(request):
#     # View for about-us page
#     user_queryset = User.objects.all()
#     full_name_list = []
#     for user in user_queryset:
#         full_name_list.append(user.get_full_name())

#     return render(request , "about_us.html" , context = {"full_name_list" : full_name_list})


