from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.destinations.models import Destination
from apps.hotels.models import Hotel
from apps.attractions.models import Attraction
from django.core.exceptions import ValidationError

class BaseImage(models.Model):
    alt_text = models.CharField(_('alt text'), max_length=255, blank=True)
    caption = models.CharField(_('caption'), max_length=255, blank=True)
    display_order = models.PositiveSmallIntegerField(_('display order'), default=0)
    is_primary = models.BooleanField(_('is primary'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        abstract = True
        ordering = ['display_order', 'created_at']

class DestinationImage(BaseImage):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(_('image'), upload_to='destinations/')

    class Meta:
        verbose_name = _('destination image')
        verbose_name_plural = _('destination images')
        indexes = [models.Index(fields=['destination', 'is_primary', 'display_order'])]

    def save(self, *args, **kwargs):
        if self.is_primary:
            DestinationImage.objects.filter(destination=self.destination).update(is_primary=False)
        super().save(*args, **kwargs)

class HotelImage(BaseImage):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(_('image'), upload_to='hotels/')

    class Meta:
        verbose_name = _('hotel image')
        verbose_name_plural = _('hotel images')
        indexes = [models.Index(fields=['hotel', 'is_primary', 'display_order'])]

    def save(self, *args, **kwargs):
        if self.is_primary:
            HotelImage.objects.filter(hotel=self.hotel).update(is_primary=False)
        super().save(*args, **kwargs)

class AttractionImage(BaseImage):
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(_('image'), upload_to='attractions/')

    class Meta:
        verbose_name = _('attraction image')
        verbose_name_plural = _('attraction images')
        indexes = [models.Index(fields=['attraction', 'is_primary', 'display_order'])]

    def save(self, *args, **kwargs):
        if self.is_primary:
            AttractionImage.objects.filter(attraction=self.attraction).update(is_primary=False)
        super().save(*args, **kwargs)
