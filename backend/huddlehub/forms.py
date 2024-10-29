from django.forms import DateInput, ModelForm, Textarea, TextInput

from .models import Event


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["title", "date", "description"]
        widgets = {
            "title": TextInput(
                attrs={
                    "class": "form-control",
                    "id": "event-title",
                    "placeholder": "Title of Event",
                    "autofocus": True,
                    "required": True,
                }
            ),
            "description": Textarea(
                attrs={
                    "class": "form-control",
                    "id": "event-description",
                    "placeholder": "Description of Event",
                    "cols": 30,
                    "rows": 5,
                    "required": True,
                }
            ),
            "date": DateInput(attrs={"type": "date", "class": "form-control"}),
        }
