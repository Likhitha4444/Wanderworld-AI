from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.images.views import DestinationImageViewSet, HotelImageViewSet, AttractionImageViewSet

destination_image_router = DefaultRouter()
destination_image_router.register(r'images', DestinationImageViewSet, basename='destination-image')

hotel_image_router = DefaultRouter()
hotel_image_router.register(r'images', HotelImageViewSet, basename='hotel-image')

attraction_image_router = DefaultRouter()
attraction_image_router.register(r'images', AttractionImageViewSet, basename='attraction-image')

urlpatterns = [
    path('admin/destinations/<int:destination_pk>/', include(destination_image_router.urls)),
    path('admin/hotels/<int:hotel_pk>/', include(hotel_image_router.urls)),
    path('admin/attractions/<int:attraction_pk>/', include(attraction_image_router.urls)),
]
