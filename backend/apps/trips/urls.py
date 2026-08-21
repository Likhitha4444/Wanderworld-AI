from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TripViewSet, TripDayViewSet, TripActivityViewSet, TripRevisionViewSet

router = DefaultRouter()
router.register(r'', TripViewSet, basename='trip')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:trip_pk>/days/', TripDayViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<int:trip_pk>/days/<int:pk>/', TripDayViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    
    path('<int:trip_pk>/days/<int:day_pk>/activities/', TripActivityViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<int:trip_pk>/days/<int:day_pk>/activities/<int:pk>/', TripActivityViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    
    path('<int:trip_pk>/revisions/', TripRevisionViewSet.as_view({'get': 'list'})),
    path('<int:trip_pk>/revisions/<int:pk>/', TripRevisionViewSet.as_view({'get': 'retrieve'})),
]
