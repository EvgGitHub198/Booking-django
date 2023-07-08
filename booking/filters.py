import django_filters
from rooms.models import Room


class BookingFilter(django_filters.FilterSet):
    class Meta:
        model = Room
        fields = {
            "price": ["exact", "lte", "gte"],
            "capacity": ["exact", "lte", "gte"],
        }
