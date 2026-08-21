from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.destinations.models import Destination

class Hotel(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', _('Draft')),
        ('PUBLISHED', _('Published')),
        ('ARCHIVED', _('Archived')),
    )

    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='hotels')
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), unique=True, max_length=255)
    description = models.TextField(_('description'))
    short_description = models.CharField(_('short description'), max_length=255)
    address = models.CharField(_('address'), max_length=255)
    city = models.CharField(_('city'), max_length=100)
    country = models.CharField(_('country'), max_length=100)
    latitude = models.DecimalField(
        _('latitude'), 
        max_digits=9, 
        decimal_places=6,
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )
    longitude = models.DecimalField(
        _('longitude'), 
        max_digits=9, 
        decimal_places=6,
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )
    star_rating = models.PositiveSmallIntegerField(_('star rating'), validators=[MinValueValidator(1), MaxValueValidator(5)])
    average_rating = models.DecimalField(_('average rating'), max_digits=3, decimal_places=2, default=0.00)
    review_count = models.PositiveIntegerField(_('review count'), default=0)
    price_per_night = models.DecimalField(
        _('price per night'), 
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    currency = models.CharField(_('currency'), max_length=3, default='USD')
    image_url = models.URLField(_('image URL'), max_length=1024, blank=True)
    amenities = models.JSONField(_('amenities'), default=list, blank=True)
    status = models.CharField(_('status'), max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    is_featured = models.BooleanField(_('is featured'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('hotel')
        verbose_name_plural = _('hotels')
        unique_together = ('destination', 'name')
        indexes = [
            models.Index(fields=['destination', 'slug']),
            models.Index(fields=['city']),
            models.Index(fields=['country']),
            models.Index(fields=['status']),
            models.Index(fields=['star_rating']),
            models.Index(fields=['is_featured']),
        ]

    def __str__(self):
        return self.name

class Room(models.Model):
    ROOM_TYPE_CHOICES = (
        ('STANDARD', _('Standard')),
        ('DELUXE', _('Deluxe')),
        ('SUITE', _('Suite')),
        ('FAMILY', _('Family')),
    )
    STATUS_CHOICES = (
        ('ACTIVE', _('Active')),
        ('INACTIVE', _('Inactive')),
    )

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(_('name'), max_length=255)
    room_type = models.CharField(_('room type'), max_length=20, choices=ROOM_TYPE_CHOICES)
    description = models.TextField(_('description'), blank=True)
    capacity = models.PositiveSmallIntegerField(_('capacity'), validators=[MinValueValidator(1)])
    bed_type = models.CharField(_('bed type'), max_length=50, blank=True)
    price_per_night = models.DecimalField(
        _('price per night'), 
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    currency = models.CharField(_('currency'), max_length=3, default='USD')
    total_rooms = models.PositiveSmallIntegerField(_('total rooms'), validators=[MinValueValidator(1)])
    available_rooms = models.PositiveSmallIntegerField(_('available rooms'), validators=[MinValueValidator(0)])
    amenities = models.JSONField(_('amenities'), default=list, blank=True)
    status = models.CharField(_('status'), max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('room')
        verbose_name_plural = _('rooms')
        indexes = [
            models.Index(fields=['hotel', 'status']),
            models.Index(fields=['room_type']),
            models.Index(fields=['price_per_night']),
        ]

    def __str__(self):
        return f"{self.name} - {self.hotel.name}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.available_rooms > self.total_rooms:
            raise ValidationError({'available_rooms': _('Available rooms cannot exceed total rooms.')})
