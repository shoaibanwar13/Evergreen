from django.contrib import admin
from .models import *

admin.site.register(CompanyDetail)
admin.site.register(Profile)
admin.site.register(Manufacturing)
admin.site.register(DailyProduction) 
admin.site.register(Client)

# Register your models here.
