from django.contrib import admin
from .models import DestinationImage, HotelImage, AttractionImage

@admin.register(DestinationImage)
class DestinationImageAdmin(admin.ModelAdmin):
    list_display = ('destination', 'is_primary', 'display_order', 'created_at')
    list_filter = ('is_primary', 'destination')

@admin.register(HotelImage)
class HotelImageAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'is_primary', 'display_order', 'created_at')
    list_filter = ('is_primary', 'hotel')

@admin.register(AttractionImage)
class AttractionImageAdmin(admin.ModelAdmin):
    list_display = ('attraction', 'is_primary', 'display_order', 'created_at')
    list_filter = ('is_primary', 'attraction')
