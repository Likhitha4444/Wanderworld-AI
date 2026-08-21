from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.destinations.models import Destination
from apps.hotels.models import Hotel
from apps.attractions.models import Attraction

class TravelDNACategory(models.Model):
    name = models.CharField(_('name'), max_length=50, unique=True)
    slug = models.SlugField(_('slug'), unique=True, max_length=50)
    description = models.TextField(_('description'), blank=True)
    is_active = models.BooleanField(_('is active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('travel DNA category')
        verbose_name_plural = _('travel DNA categories')
        indexes = [models.Index(fields=['slug'])]

    def __str__(self):
        return self.name

class UserTravelDNA(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='travel_dna')
    category = models.ForeignKey(TravelDNACategory, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(_('score'), validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    confidence = models.FloatField(_('confidence'), validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], default=0.0)
    last_calculated_at = models.DateTimeField(_('last calculated at'), auto_now=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('user travel DNA')
        verbose_name_plural = _('user travel DNA')
        unique_together = ['user', 'category']
        indexes = [models.Index(fields=['user', 'score'])]

class TravelBehaviorEvent(models.Model):
    EVENT_TYPES = (
        ('DESTINATION_VIEW', _('Destination View')),
        ('HOTEL_VIEW', _('Hotel View')),
        ('ATTRACTION_VIEW', _('Attraction View')),
        ('SEARCH', _('Search')),
        ('WISHLIST_ADD', _('Wishlist Add')),
        ('WISHLIST_REMOVE', _('Wishlist Remove')),
        ('REVIEW_SUBMITTED', _('Review Submitted')),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='behavior_events')
    event_type = models.CharField(_('event type'), max_length=20, choices=EVENT_TYPES)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, null=True, blank=True)
    metadata = models.JSONField(_('metadata'), default=dict, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('travel behavior event')
        verbose_name_plural = _('travel behavior events')
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['user', 'event_type']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.event_type}"
