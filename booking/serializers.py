from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Booking
from rooms.serializers import RoomSerializer


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    room = RoomSerializer()

    class Meta:
        model = Booking
        fields = ['id', 'user', 'room', 'start_date', 'end_date']
