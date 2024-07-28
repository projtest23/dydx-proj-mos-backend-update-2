from django.urls import path, include
from . import views

app_name = "dydx"


urlpatterns = [
    path("api/v1/", include("dydx.api.v1.urls")),
]