from django.contrib import admin
from django.urls import path, include
from rest_framework.response import Response
from rest_framework.views import APIView

class HealthCheckView(APIView):
    def get(self, request):
        return Response({"status": "ok", "service": "wanderworld-backend"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/health/', HealthCheckView.as_view(), name='health-check'),
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/', include('apps.destinations.urls')),
    path('api/v1/', include('apps.hotels.urls')),
    path('api/v1/', include('apps.attractions.urls')),
    path('api/v1/', include('apps.images.urls')),
    path('api/v1/', include('apps.search.urls')),
    path('api/v1/', include('apps.wishlist.urls')),
    path('api/v1/', include('apps.reviews.urls')),
    path('api/v1/', include('apps.travel_dna.urls')),
    path('api/v1/', include('apps.recommendations.urls')),
    path('api/v1/trips/', include('apps.trips.urls')),
]
