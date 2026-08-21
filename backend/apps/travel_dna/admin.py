from django.contrib import admin
from .models import TravelDNACategory, UserTravelDNA

@admin.register(TravelDNACategory)
class TravelDNACategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(UserTravelDNA)
class UserTravelDNAAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'score', 'confidence', 'last_calculated_at')
    list_filter = ('category',)
    search_fields = ('user__email',)
