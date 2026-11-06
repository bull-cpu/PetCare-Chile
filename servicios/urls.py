

from django.urls import path
from . import views

urlpatterns = [
    path("", views.catalogo, name="catalogo"),

    path(
        "servicio/<slug:codigo>/",
        views.detalle_servicio,
        name="detalle_servicio"
    ),
]
