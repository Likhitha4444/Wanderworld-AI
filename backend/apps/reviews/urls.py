from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.reviews.views import ReviewViewSet, ReviewAdminViewSet, ReviewPublicListView

router = DefaultRouter()
router.register(r'reviews', ReviewViewSet, basename='review')

admin_router = DefaultRouter()
admin_router.register(r'reviews', ReviewAdminViewSet, basename='review-admin')

urlpatterns = [
    path('', include(router.urls)),
    path('hotels/<slug:hotel_slug>/reviews/', ReviewPublicListView.as_view({'get': 'list'}), name='hotel-reviews'),
    path('attractions/<slug:attraction_slug>/reviews/', ReviewPublicListView.as_view({'get': 'list'}), name='attraction-reviews'),
    path('admin/', include(admin_router.urls)),
]
