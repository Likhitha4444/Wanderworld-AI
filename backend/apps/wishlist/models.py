from django.db import models
from django.conf import settings
from django.db.models import Q, CheckConstraint, UniqueConstraint, Index
from django.utils.translation import gettext_lazy as _
from apps.destinations.models import Destination
from apps.hotels.models import Hotel
from apps.attractions.models import Attraction

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('wishlist entry')
        verbose_name_plural = _('wishlist entries')
        constraints = [
            UniqueConstraint(fields=['user', 'destination'], condition=Q(destination__isnull=False), name='unique_user_destination'),
            UniqueConstraint(fields=['user', 'hotel'], condition=Q(hotel__isnull=False), name='unique_user_hotel'),
            UniqueConstraint(fields=['user', 'attraction'], condition=Q(attraction__isnull=False), name='unique_user_attraction')
        ]
        indexes = [Index(fields=['user', 'created_at'])]

    def __str__(self):
        return f"{self.user.email}'s wishlist item"

    def clean(self):
        targets = [self.destination, self.hotel, self.attraction]
        if sum(t is not None for t in targets) != 1:
            raise ValidationError(_('Exactly one of destination, hotel, or attraction must be set.'))
