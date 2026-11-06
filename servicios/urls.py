from django.urls import path
from . import views

urlpatterns = [
    # Catálogo público
    path("", views.catalogo, name="catalogo"),
    path(
        "servicio/<slug:codigo>/",
        views.detalle_servicio,
        name="detalle_servicio"
    ),

    # Carrito de solicitudes
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

    # Administración de servicios
    path(
        "administracion/servicios/",
        views.administrar_servicios,
        name="administrar_servicios"
    ),
    path(
        "administracion/servicios/crear/",
        views.crear_servicio,
        name="crear_servicio"
    ),
    path(
        "administracion/servicios/editar/<int:servicio_id>/",
        views.editar_servicio,
        name="editar_servicio"
    ),
    path(
        "administracion/servicios/eliminar/<int:servicio_id>/",
        views.eliminar_servicio,
        name="eliminar_servicio"
    ),
]