from apps.hotels.models import Hotel
print(f'Goa: {Hotel.objects.filter(destination__name="Goa").count()}')
print(f'Paris: {Hotel.objects.filter(destination__name="Paris").count()}')
