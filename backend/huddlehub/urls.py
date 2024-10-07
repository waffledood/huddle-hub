from django.urls import path

from . import views

urlpatterns = [
    path(route="home/", view=views.index, name="index"),
    path(route="create/", view=views.create, name="create"),
    path(route="login/", view=views.login_view, name="login"),
    path(route="logout/", view=views.logout_view, name="logout"),
    path(route="register/", view=views.register, name="register"),
    path(route="create/", view=views.create, name="create"),
]
