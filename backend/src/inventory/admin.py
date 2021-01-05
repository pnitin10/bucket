from django.contrib import admin
from .models import Task, Bucket

# Register your models here.

admin.site.register(Task)
admin.site.register(Bucket)