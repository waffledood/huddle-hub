from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser, UserManager


class User(AbstractUser):
    objects = UserManager()
    pass


class Event(models.Model):
    title = models.CharField(max_length=256)
    date = models.DateTimeField()
    description = models.TextField()
    organizer = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="events"
    )
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"Event ({self.id}): {self.title} organized by {self.organizer.get_username()}"


class RSVP(models.Model):
    participant = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="RSVPs"
    )
    event = models.ForeignKey(to=Event, on_delete=models.CASCADE, related_name="RSVPs")
    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"RSVP ({self.id}): {self.participant.get_username()} attending Event {self.event.id}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["participant", "event"], name="unique_RSVP")
        ]
