from rooms.models import Room
from .models import Booking


def check_room_availability(room, start_date, end_date):
    # Check if the room is available for booking for the specified dates
    overlapping_bookings = Booking.objects.filter(
        room=room, start_date__lte=end_date, end_date__gte=start_date
    )

    return not overlapping_bookings.exists()


def available_rooms(start_date, end_date):
    not_free_rooms = (
        Booking.objects.filter(start_date__lte=start_date, end_date__gte=end_date)
        | Booking.objects.filter(start_date__gte=start_date, start_date__lt=end_date)
        | Booking.objects.filter(end_date__lte=start_date, end_date__gte=end_date)
    )
    queryset = Room.objects.exclude(pk__in=not_free_rooms.values("room_id"))
    return queryset
