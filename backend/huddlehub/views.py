from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .exceptions import InvalidUserActionException
from .forms import EventForm
from .models import Event, RSVP, User


def loadEvents(request, events):
    eventsWithRSVPInfo = list()

    if request.user.is_authenticated:
        # check if user has already RSVP'ed for existing Events
        for event in events:
            existingRSVP = list(
                RSVP.objects.filter(participant__exact=request.user).filter(
                    event__exact=event
                )
            )

            hasRSVPedForEvent = False if len(existingRSVP) == 0 else True

            # eventsWithRSVPInfo is a list of the tuple (Event, boolean indicating
            # if the user sending this request has RSVP'ed for the Event)
            eventsWithRSVPInfo.append((event, hasRSVPedForEvent))

    return eventsWithRSVPInfo


def index(request):
    events = list(Event.objects.all())

    eventsWithRSVPInfo = loadEvents(request, events)

    return render(
        request=request,
        template_name="index.html",
        context={"events": eventsWithRSVPInfo},
    )


@login_required(login_url="/login/")
def create(request):
    pass


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication is successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auth/login.html",
                {"message": "Invalid credentials."},
            )
    else:
        return render(request, "auth/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(
                request, "auth/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auth/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auth/register.html")


def create(request):
    if request.method == "POST":
        event = EventForm(request.POST)
        if event.is_valid():
            pendingEvent = event.save(commit=False)
            # Add user submitting this request as organizer for this event
            pendingEvent.organizer = request.user
            pendingEvent.save()
            event.save_m2m()

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request, "create.html", {"message": "Details of Event are incorrect"}
            )
    else:
        return render(request, "create.html", {"eventForm": EventForm()})


def event(request, eventId):
    try:
        event = Event.objects.get(id=eventId)
    except Event.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))

    return render(request, "event.html", {"event": event})


def rsvp(request, eventId):
    if request.method == "POST":
        try:
            eventToRSVPFor = Event.objects.get(id=eventId)

            organizerOfEventToRSVPFor = eventToRSVPFor.organizer

            # throw an Exception if the user tries to RSVP for their own Event
            if request.user == organizerOfEventToRSVPFor:
                raise InvalidUserActionException()

            # check if user has already RSVP'ed for the event
            existingRSVP = RSVP.objects.filter(participant__exact=request.user).filter(
                event__exact=eventToRSVPFor
            )
            rsvp = existingRSVP.get()

            # remove the RSVP if there exists one
            rsvp.delete()
            print(f"RSVP removed for {request.user.username} for {eventToRSVPFor}")

        except InvalidUserActionException as e:
            print(f"{e}")

        # if there doesn't exist an Event, exit this view
        except Event.DoesNotExist:
            print(f"Request event with id {eventId} does not exist")

        # if there doesn't exist an RSVP, create one
        except RSVP.DoesNotExist:
            try:
                rsvp = RSVP(participant=request.user, event=eventToRSVPFor)
                rsvp.save()
                print(f"RSVP created for {request.user.username} for {eventToRSVPFor}")
            except IntegrityError:
                print(
                    f"RSVP already created for {request.user.username} for {eventToRSVPFor}"
                )

        return HttpResponseRedirect(reverse("index"))

    else:
        return HttpResponseRedirect(reverse("index"))
