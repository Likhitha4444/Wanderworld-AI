from django.contrib import admin
from .models import Destination

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'status', 'is_featured', 'created_at')
    list_filter = ('status', 'is_featured', 'country')
    search_fields = ('name', 'city', 'country')
