import django_filters
from .models import Room


class RoomFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    capacity = django_filters.CharFilter(
        field_name="capacity", method="filter_capacity"
    )

    class Meta:
        model = Room
        fields = ["min_price", "max_price", "capacity"]

    def filter_capacity(self, queryset, name, value):
        capacities = value.split(",")
        capacities = [int(capacity) for capacity in capacities]
        return queryset.filter(capacity__in=capacities)
