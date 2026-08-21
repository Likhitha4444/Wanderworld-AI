from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from django.core.exceptions import ObjectDoesNotExist
from apps.reviews.models import Review


@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_target_rating(sender, instance, **kwargs):

    # Safely get the hotel
    try:
        hotel = instance.hotel
    except ObjectDoesNotExist:
        hotel = None

    # Safely get the attraction
    try:
        attraction = instance.attraction
    except ObjectDoesNotExist:
        attraction = None

    # If the related target was already deleted, there is nothing to update
    if not hotel and not attraction:
        return

    # Determine which target this review belongs to
    target = hotel or attraction

    # Get published reviews for the same target
    if hotel:
        published_reviews = Review.objects.filter(
            hotel=hotel,
            status='PUBLISHED'
        )
    else:
        published_reviews = Review.objects.filter(
            attraction=attraction,
            status='PUBLISHED'
        )

    # Calculate rating statistics
    stats = published_reviews.aggregate(
        average=Avg('rating'),
        count=models.Count('id')
    )

    target.average_rating = stats['average'] or 0.00
    target.review_count = stats['count'] or 0
    target.save()