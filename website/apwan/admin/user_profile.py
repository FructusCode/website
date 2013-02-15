# pylint: disable=R0904

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import models
from website.apwan.models.user_profile import UserProfile

__author__ = 'Dean Gardiner'


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = "user"
    max_num = 1
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

    def save_model(self, request, obj, form, change):
        obj.save()
        profile = None
        try:
            profile = obj.get_profile()
        except BaseException, e:
            if isinstance(e, UserProfile.DoesNotExist):
                profile = UserProfile(user=obj)

        if profile is not None:
            profile.save()

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
