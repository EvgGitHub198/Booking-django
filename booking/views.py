
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import CustomUser
from .models import Booking
from .serializers import BookingSerializer
from .utils import check_room_availability
from rooms.models import Room
from rooms.serializers import RoomSerializer
from rest_framework import generics, status
from rest_framework.response import Response


class BookingCreateAPIView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def post(self, request, *args, **kwargs):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        min_price = request.data.get('min_price')
        max_price = request.data.get('max_price')
        capacities = request.data.get('capacity')

        available_rooms = self.get_available_rooms(start_date, end_date, min_price, max_price, capacities)

        serializer = RoomSerializer(available_rooms, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_available_rooms(self, start_date, end_date, min_price, max_price, capacities):

        booked_room_ids = Booking.objects.filter(
            start_date__lte=end_date, end_date__gte=start_date
        ).values_list('room_id', flat=True)

        available_rooms = Room.objects.exclude(id__in=booked_room_ids)

        if min_price and max_price:
            available_rooms = available_rooms.filter(price__range=(min_price, max_price))
        elif min_price:
            available_rooms = available_rooms.filter(price__gte=min_price)
        elif max_price:
            available_rooms = available_rooms.filter(price__lte=max_price)

        if capacities:
            capacities_list = capacities.split(',')
            available_rooms = available_rooms.filter(capacity__in=capacities_list)

        return available_rooms


class BookingReservationAPIView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        user = CustomUser.objects.get(email=request.user.email)
        room_id = request.data.get('room_id')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        if not room_id:
            return Response({"error": "Room ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        if not check_room_availability(room_id, start_date, end_date):
            return Response({"error": "Room is not available for the selected dates."}, status=status.HTTP_400_BAD_REQUEST)

        booking = Booking.objects.create(user=user, room_id=room_id, start_date=start_date, end_date=end_date)
        serializer = BookingSerializer(booking)

        return Response(serializer.data, status=status.HTTP_201_CREATED)