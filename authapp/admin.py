from django.contrib import admin
from .models import AbstractUser, ShopUser, ShopUserProfile


# Register your models here.

class AbstractUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_active')
    list_display_links = ('username', 'first_name', 'last_name', 'email')
    search_fields = ('username', 'first_name', 'last_name', 'email')


admin.site.register(ShopUser, AbstractUserAdmin)


class ShopUserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'tagline', 'aboutMe', 'gender')
    list_display_links = ('user', 'tagline', 'aboutMe', 'gender')
    search_fields = ('user', 'tagline', 'aboutMe', 'gender')


admin.site.register(ShopUserProfile, ShopUserProfileAdmin)
