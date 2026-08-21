from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.travel_dna.views import TravelDNAViewSet, BehaviorEventViewSet

router = DefaultRouter()
router.register(r'travel-dna', TravelDNAViewSet, basename='travel-dna')
router.register(r'behavior/events', BehaviorEventViewSet, basename='behavior-event')

urlpatterns = [
    path('', include(router.urls)),
]
