from django.test import TestCase
from rest_framework.test import APIClient
from datetime import date
from .models import Booking
from users.models import CustomUser
from rooms.models import Room
from .serializers import BookingSerializer


class BookingModelTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email="test@example.com", password="test123"
        )
        self.room = Room.objects.create(number="101", price=100, capacity=2)
        self.booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            start_date=date.today(),
            end_date=date.today(),
        )

    def test_booking_creation(self):
        self.assertEqual(
            str(self.booking),
            f"{self.user} | {self.room} room: from {date.today()} to {date.today()}",
        )


class BookingViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(
            email="test@example.com", password="test123"
        )
        self.room = Room.objects.create(number="101", price=100, capacity=2)
        self.booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            start_date=date.today(),
            end_date=date.today(),
        )

    def test_booking_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/v1/user-bookings/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_booking_cancel(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            f"/api/v1/user-bookings/{self.booking.pk}/cancel/"
        )
        self.assertEqual(response.status_code, 204)


class BookingSerializerTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email="test@example.com", password="test123"
        )
        self.room = Room.objects.create(number="101", price=100, capacity=2)
        self.booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            start_date=date.today(),
            end_date=date.today(),
        )

    def test_booking_serialization(self):
        serializer_data = BookingSerializer(instance=self.booking).data
        self.assertEqual(serializer_data["user"]["email"], "test@example.com")
        self.assertEqual(serializer_data["room"]["number"], "101")
        self.assertEqual(serializer_data["start_date"], str(date.today()))
        self.assertEqual(serializer_data["end_date"], str(date.today()))
