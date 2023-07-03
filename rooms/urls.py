from django.urls import path
from .views import RoomListAPIView, RoomDetailAPIView

urlpatterns = [
    path("rooms/", RoomListAPIView.as_view(), name="room-list"),
    path("rooms/<str:number>/", RoomDetailAPIView.as_view(), name="room-detail"),
]
