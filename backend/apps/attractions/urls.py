from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.attractions.views import AttractionPublicViewSet, AttractionAdminViewSet

router = DefaultRouter()
router.register(r'attractions', AttractionPublicViewSet, basename='attraction-public')

admin_router = DefaultRouter()
admin_router.register(r'attractions', AttractionAdminViewSet, basename='attraction-admin')

urlpatterns = [
    path('', include(router.urls)),
    path('destinations/<slug:destination_slug>/attractions/', AttractionPublicViewSet.as_view({'get': 'list'}), name='destination-attraction-public-list'),
    path('admin/', include(admin_router.urls)),
]
