from django.urls import path

from . import views

urlpatterns = [
    path(route="home/", view=views.index, name="index"),
    path(route="create/", view=views.create, name="create"),
    path(route="login/", view=views.login_view, name="login"),
]
