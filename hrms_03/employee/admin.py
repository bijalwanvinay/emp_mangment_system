from django.contrib import admin
from .models import EmployeeDetail, Leave

# Register your models here.
admin.site.register(EmployeeDetail)

admin.site.register(Leave)

