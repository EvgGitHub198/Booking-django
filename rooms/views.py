from drf_spectacular.utils import extend_schema
from rest_framework import generics
from .filters import RoomFilter
from .models import Room
from .serializers import RoomSerializer


@extend_schema(
    tags=["Rooms"],
    description="Get a list of rooms",
)
class RoomListAPIView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filterset_class = RoomFilter
    ordering_fields = ("price",)

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.query_params.get("sort_by")
        if sort_by == "price_desc":
            queryset = queryset.order_by("-price")
        elif sort_by == "price_asc":
            queryset = queryset.order_by("price")
        return queryset


@extend_schema(
    tags=["Rooms"],
    description="Get details of a room",
)
class RoomDetailAPIView(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = "number"
