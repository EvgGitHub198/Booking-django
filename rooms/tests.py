from django.test import TestCase
from .models import Room
from .serializers import RoomSerializer
from rest_framework.test import APIClient


class RoomModelTestCase(TestCase):
    def test_room_creation(self):
        room = Room.objects.create(number="101", price=100, capacity=2)
        self.assertEqual(room.number, "101")
        self.assertEqual(room.price, 100)
        self.assertEqual(room.capacity, 2)


class RoomViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        Room.objects.create(number="101", price=100, capacity=2)
        Room.objects.create(number="102", price=150, capacity=4)

    def test_room_list(self):
        response = self.client.get("/api/v1/rooms/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_room_detail(self):
        response = self.client.get("/api/v1/rooms/101/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["number"], "101")

    def test_room_filtering(self):
        response = self.client.get("/api/v1/rooms/?min_price=100&capacity=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["number"], "101")

    def test_room_sorting(self):
        response = self.client.get("/api/v1/rooms/?sort_by=price_asc")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["number"], "101")

    def test_room_serialization(self):
        room = Room.objects.get(number="101")
        serializer = RoomSerializer(room)
        self.assertEqual(serializer.data["number"], "101")
        self.assertEqual(serializer.data["price"], "100.00")
        self.assertEqual(serializer.data["capacity"], 2)
