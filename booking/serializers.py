from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Booking
from rooms.serializers import RoomSerializer


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    room = RoomSerializer()

    class Meta:
        model = Booking
        fields = ["id", "user", "room", "start_date", "end_date"]
