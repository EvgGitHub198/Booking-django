from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rooms.models import Room
from users.models import CustomUser
from .filters import BookingFilter
from .models import Booking
from .serializers import BookingSerializer
from .utils import check_room_availability, available_rooms
from rooms.serializers import RoomSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter


@extend_schema(
    tags=["Booking"],
    description="Search for available rooms based on specified dates and filters",
    request=BookingSerializer,
    responses={200: RoomSerializer(many=True)},
)
class RoomListAPIView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = BookingFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        if start_date and end_date:
            return available_rooms(start_date, end_date)
        return queryset


@extend_schema(
    tags=["Booking"], description="Creating a Booking", request=BookingSerializer
)
class BookingReservationAPIView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = CustomUser.objects.get(email=request.user.email)
        room_id = request.data.get("room_id")
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")

        if not room_id:
            return Response(
                {"error": "Room ID is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        if not check_room_availability(room_id, start_date, end_date):
            return Response(
                {"error": "Room is not available for the selected dates."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        booking = Booking.objects.create(
            user=user, room_id=room_id, start_date=start_date, end_date=end_date
        )
        serializer = BookingSerializer(booking)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=["Booking"], description="User's booking list", request=BookingSerializer
)
class BookingListAPIView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(user=user)


@extend_schema(
    tags=["Booking"], description="Cancel a Booking", request=BookingSerializer
)
class BookingCancelAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer

    def delete(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
            booking.delete()
            return Response(
                {"message": "Booking successfully canceled."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Booking.DoesNotExist:
            return Response(
                {
                    "error": "Booking not found or you don't have permission to cancel it."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
