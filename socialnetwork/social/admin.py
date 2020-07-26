from django.contrib import admin
from .models import SocialUser


@admin.register(SocialUser)
class UserAdmin(admin.ModelAdmin):
    pass
