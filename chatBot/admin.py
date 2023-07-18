from django.contrib import admin
from .models import test
# Register your models here.

admin.register(test, site=admin.site)
