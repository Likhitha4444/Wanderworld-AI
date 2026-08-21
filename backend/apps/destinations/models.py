from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class Destination(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', _('Draft')),
        ('PUBLISHED', _('Published')),
        ('ARCHIVED', _('Archived')),
    )

    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), unique=True, max_length=255)
    country = models.CharField(_('country'), max_length=100)
    region = models.CharField(_('region'), max_length=100, blank=True)
    city = models.CharField(_('city'), max_length=100)
    description = models.TextField(_('description'))
    short_description = models.CharField(_('short description'), max_length=255)
    
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
    
    cover_image_url = models.URLField(_('cover image URL'), blank=True)
    best_time_to_visit = models.CharField(_('best time to visit'), max_length=255, blank=True)
    average_budget = models.DecimalField(
        _('average budget'), 
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    currency = models.CharField(_('currency'), max_length=3, default='USD')
    
    status = models.CharField(_('status'), max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    is_featured = models.BooleanField(_('is featured'), default=False)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now_add=True)

    class Meta:
        verbose_name = _('destination')
        verbose_name_plural = _('destinations')
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['city']),
            models.Index(fields=['country']),
            models.Index(fields=['status']),
            models.Index(fields=['is_featured']),
        ]

    def __str__(self):
        return f"{self.name}, {self.city}, {self.country}"
