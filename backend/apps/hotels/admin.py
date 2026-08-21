from django.contrib import admin
from .models import Hotel, Room

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'destination', 'status', 'is_featured')
    list_filter = ('status', 'is_featured', 'destination', 'star_rating')
    search_fields = ('name', 'city', 'country')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotel', 'room_type', 'capacity', 'price_per_night', 'status')
    list_filter = ('status', 'room_type', 'hotel')
    search_fields = ('name', 'hotel__name')
