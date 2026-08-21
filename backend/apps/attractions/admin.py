from django.contrib import admin
from .models import Attraction

@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'destination', 'category', 'status', 'is_featured')
    list_filter = ('status', 'is_featured', 'destination', 'category')
    search_fields = ('name', 'city', 'country')
