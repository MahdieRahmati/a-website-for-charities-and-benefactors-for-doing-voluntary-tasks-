from django.contrib import admin
from charities.models import Charity , Benefactor , Task
# Register your models here.

admin.site.register(Charity)
admin.site.register(Benefactor)
admin.site.register(Task)
