from django.urls import path

from . import views

urlpatterns = [path(route="home/", view=views.main, name="main")]
