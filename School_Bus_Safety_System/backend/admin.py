from django.contrib import admin

# Register your models here.
from .models import Student,TravelStatus

admin.site.register(Student)
admin.site.register(TravelStatus)
