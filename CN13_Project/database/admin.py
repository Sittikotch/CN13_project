from django.contrib import admin
from .models import *

# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ("userId", "sid", "fname", "lname","tel","dept")

admin.site.register(Student, StudentAdmin)