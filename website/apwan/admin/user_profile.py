# pylint: disable=R0904

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from website.apwan.models.user_profile import UserProfile

__author__ = 'Dean Gardiner'


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = "user"
    max_num = 1
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
