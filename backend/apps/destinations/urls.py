from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.destinations.views import DestinationPublicViewSet, DestinationAdminViewSet

router = DefaultRouter()
router.register(r'destinations', DestinationPublicViewSet, basename='destination-public')
admin_router = DefaultRouter()
admin_router.register(r'destinations', DestinationAdminViewSet, basename='destination-admin')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', include(admin_router.urls)),
]
