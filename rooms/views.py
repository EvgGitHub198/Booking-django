from rest_framework import generics
from .models import Room
from .serializers import RoomSerializer


class RoomListAPIView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        capacities = self.request.query_params.get('capacity')
        if capacities:
            capacities = capacities.split(',')
            capacities = [int(capacity) for capacity in capacities]
            queryset = queryset.filter(capacity__in=capacities)

        sort_by = self.request.query_params.get('sort_by')
        if sort_by == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_desc':
            queryset = queryset.order_by('-price')

        return queryset


class RoomDetailAPIView(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'number'