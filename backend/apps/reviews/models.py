from django.db import models
from django.conf import settings
from django.db.models import Q, CheckConstraint, UniqueConstraint, Index
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.hotels.models import Hotel
from apps.attractions.models import Attraction

class Review(models.Model):
    STATUS_CHOICES = (
        ('PENDING', _('Pending')),
        ('PUBLISHED', _('Published')),
        ('REJECTED', _('Rejected')),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(_('rating'), validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(_('title'), max_length=255, blank=True)
    comment = models.TextField(_('comment'))
    status = models.CharField(_('status'), max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('review')
        verbose_name_plural = _('reviews')
        constraints = [
            UniqueConstraint(fields=['user', 'hotel'], condition=Q(hotel__isnull=False), name='unique_user_hotel_review'),
            UniqueConstraint(fields=['user', 'attraction'], condition=Q(attraction__isnull=False), name='unique_user_attraction_review')
        ]
        indexes = [
            Index(fields=['hotel', 'status']),
            Index(fields=['attraction', 'status']),
            Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f"{self.user.email} - {'Hotel' if self.hotel else 'Attraction'} Review"

    def clean(self):
        from django.core.exceptions import ValidationError
        targets = [self.hotel, self.attraction]
        if sum(t is not None for t in targets) != 1:
            raise ValidationError(_('Exactly one of hotel or attraction must be set.'))
