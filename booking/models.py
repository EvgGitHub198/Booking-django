from django.db import models
from users.models import CustomUser
from rooms.models import Room


class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.user} | {self.room} room: from {self.start_date} to {self.end_date}"

