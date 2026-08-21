from django.contrib import admin
from .models import Trip, TripDay, TripActivity, TripRevision

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'destination', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'planning_source')
    search_fields = ('title', 'user__username')

@admin.register(TripDay)
class TripDayAdmin(admin.ModelAdmin):
    list_display = ('trip', 'day_number', 'date')
    list_filter = ('trip',)

@admin.register(TripActivity)
class TripActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'trip_day', 'activity_type', 'start_time', 'end_time')
    list_filter = ('activity_type',)

@admin.register(TripRevision)
class TripRevisionAdmin(admin.ModelAdmin):
    list_display = ('trip', 'revision_number', 'created_by', 'created_at')
    list_filter = ('trip',)
