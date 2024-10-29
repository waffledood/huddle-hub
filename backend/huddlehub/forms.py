from django.forms import DateInput, ModelForm

from .models import Event


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["title", "date", "description"]

        widgets = {
            "date": DateInput(attrs={"type": "date"}),
        }
