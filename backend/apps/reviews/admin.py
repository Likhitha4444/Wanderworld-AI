from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'hotel', 'attraction', 'rating', 'status', 'created_at')
    list_filter = ('status', 'rating', 'hotel', 'attraction')
    search_fields = ('user__email', 'title', 'comment')
