import django_filters
from apps.destinations.models import Destination

class DestinationFilter(django_filters.FilterSet):
    country = django_filters.CharFilter(field_name='country', lookup_expr='iexact')

    class Meta:
        model = Destination
        fields = ['country', 'region', 'city', 'is_featured']
