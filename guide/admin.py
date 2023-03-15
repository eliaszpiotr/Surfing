from django.contrib import admin
from .models import CustomUser, UserProfile, Danger, SurfSpot


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active',)
    search_fields = ('username', 'email',)
    list_filter = ('is_staff', 'is_active',)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'country', 'home_spot',)
    search_fields = ('user__username', 'nickname', 'country',)
    list_filter = ('country',)


class DangerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class SurfSpotAdmin(admin.ModelAdmin):
    list_display = ('name', 'continent', 'country', 'spot_type', 'wave_type', 'crowd', 'difficulty',)
    search_fields = ('name', 'continent', 'country', 'spot_type', 'wave_type',)
    list_filter = ('continent',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Danger, DangerAdmin)
admin.site.register(SurfSpot, SurfSpotAdmin)
