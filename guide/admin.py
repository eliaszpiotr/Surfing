from django.contrib import admin
from django.utils.html import format_html

from .models import CustomUser, UserProfile, Danger, SurfSpot, Surfboard


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active',)
    search_fields = ('username', 'email',)
    list_filter = ('is_staff', 'is_active',)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'home_spot', 'profile_picture_thumbnail')
    search_fields = ('user__username', 'country')
    list_filter = ('country',)




class DangerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class SurfSpotAdmin(admin.ModelAdmin):
    list_display = ('name', 'continent', 'country', 'spot_type', 'wave_type', 'crowd', 'difficulty',)
    search_fields = ('name', 'continent', 'country', 'spot_type', 'wave_type',)
    list_filter = ('continent',)


class SurfboardAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'length', 'width', 'thickness', 'volume', 'construction', 'fin_setup',  'tail')
    search_fields = ('name', 'brand', 'length', 'width', 'thickness', 'volume', 'construction', 'fin_setup',  'tail')
    list_filter = ('brand', 'user')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Danger, DangerAdmin)
admin.site.register(SurfSpot, SurfSpotAdmin)
admin.site.register(Surfboard, SurfboardAdmin)
