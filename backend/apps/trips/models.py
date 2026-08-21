from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
from apps.destinations.models import Destination
from apps.attractions.models import Attraction
from apps.hotels.models import Hotel

class TripStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    GENERATING = 'GENERATING', 'Generating'
    READY = 'READY', 'Ready'
    FAILED = 'FAILED', 'Failed'
    ARCHIVED = 'ARCHIVED', 'Archived'

class PlanningSource(models.TextChoices):
    MANUAL = 'MANUAL', 'Manual'
    AI = 'AI', 'AI'
    AI_REGENERATED = 'AI_REGENERATED', 'AI Regenerated'

class Trip(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trips')
    title = models.CharField(max_length=255)
    destination = models.ForeignKey(Destination, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_travelers = models.PositiveIntegerField(default=1)
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    currency = models.CharField(max_length=3, default='INR')
    status = models.CharField(max_length=20, choices=TripStatus.choices, default=TripStatus.DRAFT)
    planning_source = models.CharField(max_length=20, choices=PlanningSource.choices, default=PlanningSource.MANUAL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Start date cannot be after end date.")
        if self.number_of_travelers < 1:
            raise ValidationError("Number of travelers must be at least 1.")

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class TripDay(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='days')
    day_number = models.PositiveIntegerField()
    date = models.DateField()
    title = models.CharField(max_length=255, blank=True)
    summary = models.TextField(blank=True)

    class Meta:
        unique_together = ['trip', 'day_number']
        ordering = ['day_number']

    def __str__(self):
        return f"{self.trip.title} - Day {self.day_number}"

class ActivityType(models.TextChoices):
    ATTRACTION = 'ATTRACTION', 'Attraction'
    MEAL = 'MEAL', 'Meal'
    HOTEL = 'HOTEL', 'Hotel'
    TRAVEL = 'TRAVEL', 'Travel'
    FREE_TIME = 'FREE_TIME', 'Free Time'
    CUSTOM = 'CUSTOM', 'Custom'

class TripActivity(models.Model):
    trip_day = models.ForeignKey(TripDay, on_delete=models.CASCADE, related_name='activities')
    attraction = models.ForeignKey(Attraction, on_delete=models.SET_NULL, null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)
    activity_type = models.CharField(max_length=20, choices=ActivityType.choices)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField()
    estimated_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    currency = models.CharField(max_length=3, default='INR')
    sequence = models.PositiveIntegerField()
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['sequence']

    def clean(self):
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time.")

    def __str__(self):
        return f"{self.trip_day.day_number} - {self.title}"

class TripRevision(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='revisions')
    revision_number = models.PositiveIntegerField()
    itinerary_snapshot = models.JSONField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    change_reason = models.TextField()

    class Meta:
        unique_together = ['trip', 'revision_number']
        ordering = ['-revision_number']

    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise ValidationError("Revisions are immutable.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.trip.title} - Revision {self.revision_number}"
