from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def index(request):
    return render(request=request, template_name="index.html", context={})


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
            return HttpResponseRedirect(reverse("main"))
        else:
            return render(
                request,
                "login.html",
                {"message": "Invalid credentials."},
            )
    else:
        return render(request, "login.html")


def logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("main"))
