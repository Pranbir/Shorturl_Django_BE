from django.contrib import admin

from .models import Urldata, Accessdata

# Register your models here.

admin.site.register(Urldata)
admin.site.register(Accessdata)