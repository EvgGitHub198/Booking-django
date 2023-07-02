from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Booking
from rooms.serializers import RoomSerializer


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    room = RoomSerializer()

    class Meta:
        model = Booking
        fields = ['id', 'user', 'room', 'start_date', 'end_date']
