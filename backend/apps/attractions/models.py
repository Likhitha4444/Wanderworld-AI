from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from apps.destinations.models import Destination

class Attraction(models.Model):
    CATEGORY_CHOICES = (
        ('HISTORICAL', _('Historical')),
        ('CULTURAL', _('Cultural')),
        ('NATURE', _('Nature')),
        ('ADVENTURE', _('Adventure')),
        ('RELIGIOUS', _('Religious')),
        ('MUSEUM', _('Museum')),
        ('BEACH', _('Beach')),
        ('PARK', _('Park')),
        ('SHOPPING', _('Shopping')),
        ('ENTERTAINMENT', _('Entertainment')),
        ('OTHER', _('Other')),
    )

    STATUS_CHOICES = (
        ('DRAFT', _('Draft')),
        ('PUBLISHED', _('Published')),
        ('ARCHIVED', _('Archived')),
    )

    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='attractions')
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), unique=True, max_length=255)
    short_description = models.CharField(_('short description'), max_length=255)
    description = models.TextField(_('description'))
    category = models.CharField(_('category'), max_length=20, choices=CATEGORY_CHOICES)
    address = models.CharField(_('address'), max_length=255, blank=True)
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
    entry_fee = models.DecimalField(
        _('entry fee'), 
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    currency = models.CharField(_('currency'), max_length=3, default='USD')
    image_url = models.URLField(_('image URL'), max_length=1024, blank=True)
    estimated_duration = models.PositiveIntegerField(_('estimated duration (mins)'), validators=[MinValueValidator(1)])
    best_time_to_visit = models.CharField(_('best time to visit'), max_length=255, blank=True)
    opening_time = models.TimeField(_('opening time'), null=True, blank=True)
    closing_time = models.TimeField(_('closing time'), null=True, blank=True)
    average_rating = models.DecimalField(
        _('average rating'), 
        max_digits=3, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    review_count = models.PositiveIntegerField(_('review count'), default=0)
    popularity_score = models.IntegerField(_('popularity score'), default=0)
    accessibility = models.JSONField(_('accessibility info'), default=dict, blank=True)
    status = models.CharField(_('status'), max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    is_featured = models.BooleanField(_('is featured'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('attraction')
        verbose_name_plural = _('attractions')
        indexes = [
            models.Index(fields=['destination', 'slug']),
            models.Index(fields=['category']),
            models.Index(fields=['city']),
            models.Index(fields=['country']),
            models.Index(fields=['status']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['popularity_score']),
            models.Index(fields=['entry_fee']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.opening_time and self.closing_time and self.opening_time >= self.closing_time:
            raise ValidationError({'closing_time': _('Closing time must be after opening time.')})
