from django.urls import path

from core import views as core_views

app_name = "core"

urlpatterns = [
    path("", core_views.receive_message, name="receive_message"),
]
