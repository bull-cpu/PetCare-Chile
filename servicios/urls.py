from django.urls import path
from . import views

urlpatterns = [
    path("", views.catalogo, name="catalogo"),

    path(
        "servicio/<slug:codigo>/",
        views.detalle_servicio,
        name="detalle_servicio"
    ),

    path("carrito/", views.ver_carrito, name="ver_carrito"),

    path(
        "carrito/agregar/<int:servicio_id>/",
        views.agregar_carrito,
        name="agregar_carrito"
    ),

    path(
        "carrito/actualizar/<int:servicio_id>/",
        views.actualizar_carrito,
        name="actualizar_carrito"
    ),

    path(
        "carrito/eliminar/<int:servicio_id>/",
        views.eliminar_carrito,
        name="eliminar_carrito"
    ),

    path(
        "carrito/vaciar/",
        views.vaciar_carrito,
        name="vaciar_carrito"
    ),
]