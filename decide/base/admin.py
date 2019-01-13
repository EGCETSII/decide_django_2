from django.contrib import admin

from .models import Auth, Key


from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User



admin.site.register(Auth)
admin.site.register(Key)


