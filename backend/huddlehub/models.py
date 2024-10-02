from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=256, default="New Event")
    organizer = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Event ({self.id}): {self.title} organized by {self.organizer.get_username()}"


class RSVP(models.Model):
    participant = models.ForeignKey(to=User, on_delete=models.CASCADE)
    event = models.ForeignKey(to=Event, on_delete=models.CASCADE, related_name="RSVPs")
    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"RSVP ({self.id}): {self.participant.get_username()} attending Event {self.event.id}"