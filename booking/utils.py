from .models import Booking


def check_room_availability(room, start_date, end_date):
    # Check if the room is available for booking for the specified dates
    overlapping_bookings = Booking.objects.filter(
        room=room,
        start_date__lte=end_date,
        end_date__gte=start_date
    )

    return not overlapping_bookings.exists()