from django.urls import path

from . import views

app_name = "entry"

urlpatterns = [
    path("<str:entry_name>", views.entry, name="entry")
]
