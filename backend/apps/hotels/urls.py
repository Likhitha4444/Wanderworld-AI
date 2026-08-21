from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.hotels.views import HotelPublicViewSet, HotelAdminViewSet, RoomPublicViewSet, RoomAdminViewSet

router = DefaultRouter()
router.register(r'hotels', HotelPublicViewSet, basename='hotel-public')

admin_router = DefaultRouter()
admin_router.register(r'hotels', HotelAdminViewSet, basename='hotel-admin')

room_admin_router = DefaultRouter()
room_admin_router.register(r'rooms', RoomAdminViewSet, basename='room-admin')

urlpatterns = [
    path('', include(router.urls)),
    path('hotels/<slug:hotel_slug>/rooms/', RoomPublicViewSet.as_view({'get': 'list'}), name='room-public-list'),
    path('destinations/<slug:destination_slug>/hotels/', HotelPublicViewSet.as_view({'get': 'list'}), name='destination-hotel-public-list'),
    path('admin/', include(admin_router.urls)),
    path('admin/hotels/<int:hotel_pk>/', include(room_admin_router.urls)),
]
