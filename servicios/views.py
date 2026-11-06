from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from decimal import Decimal

from .models import CategoriaServicio, Servicio


def catalogo(request):
    servicios = Servicio.objects.filter(
        activo=True,
        estado=Servicio.Estado.DISPONIBLE,
        categoria__activa=True
    ).select_related("categoria")

    busqueda = request.GET.get("q", "")

    if busqueda:
        servicios = servicios.filter(
            Q(nombre__icontains=busqueda) |
            Q(descripcion__icontains=busqueda) |
            Q(codigo__icontains=busqueda)
        )

    categoria_id = request.GET.get("categoria", "")

    if categoria_id:
        servicios = servicios.filter(categoria_id=categoria_id)

    orden = request.GET.get("orden", "nombre")

    if orden in ["nombre", "-nombre", "precio", "-precio"]:
        servicios = servicios.order_by(orden)
    else:
        servicios = servicios.order_by("nombre")

    paginador = Paginator(servicios, 6)
    pagina = request.GET.get("pagina")
    servicios_pagina = paginador.get_page(pagina)

    categorias = CategoriaServicio.objects.filter(activa=True)

    contexto = {
        "servicios": servicios_pagina,
        "categorias": categorias,
        "busqueda": busqueda,
        "categoria_seleccionada": categoria_id,
        "orden_seleccionado": orden,
    }

    return render(request, "servicios/catalogo.html", contexto)


def detalle_servicio(request, codigo):
    servicio = get_object_or_404(
        Servicio,
        codigo=codigo,
        activo=True,
        estado=Servicio.Estado.DISPONIBLE,
        categoria__activa=True
    )

    return render(
        request,
        "servicios/detalle.html",
        {"servicio": servicio}
    )


def ver_carrito(request):
    carrito = request.session.get("carrito", {})
    elementos = []
    total = Decimal("0.00")

    for servicio_id, cantidad in carrito.items():
        servicio = Servicio.objects.filter(
            id=servicio_id,
            activo=True,
            estado=Servicio.Estado.DISPONIBLE,
            categoria__activa=True
        ).first()

        if servicio:
            subtotal = servicio.precio * cantidad
            elementos.append({
                "servicio": servicio,
                "cantidad": cantidad,
                "subtotal": subtotal,
            })
            total += subtotal

    return render(
        request,
        "servicios/carrito.html",
        {
            "elementos": elementos,
            "total": total,
        }
    )


def agregar_carrito(request, servicio_id):
    if request.method != "POST":
        return redirect("catalogo")

    servicio = get_object_or_404(
        Servicio,
        id=servicio_id,
        activo=True,
        estado=Servicio.Estado.DISPONIBLE,
        categoria__activa=True
    )

    carrito = request.session.get("carrito", {})
    clave = str(servicio.id)

    carrito[clave] = carrito.get(clave, 0) + 1

    request.session["carrito"] = carrito
    request.session.modified = True

    messages.success(
        request,
        f"{servicio.nombre} se agregó a tu carrito."
    )

    return redirect("ver_carrito")


def actualizar_carrito(request, servicio_id):
    if request.method != "POST":
        return redirect("ver_carrito")

    carrito = request.session.get("carrito", {})
    clave = str(servicio_id)

    try:
        cantidad = int(request.POST.get("cantidad", 1))
    except (TypeError, ValueError):
        cantidad = 1

    if clave in carrito:
        if cantidad > 0:
            carrito[clave] = min(cantidad, 99)
        else:
            carrito.pop(clave)

    request.session["carrito"] = carrito
    request.session.modified = True

    messages.success(request, "Carrito actualizado.")

    return redirect("ver_carrito")


def eliminar_carrito(request, servicio_id):
    if request.method != "POST":
        return redirect("ver_carrito")

    carrito = request.session.get("carrito", {})
    carrito.pop(str(servicio_id), None)

    request.session["carrito"] = carrito
    request.session.modified = True

    messages.success(request, "Servicio eliminado del carrito.")

    return redirect("ver_carrito")


def vaciar_carrito(request):
    if request.method != "POST":
        return redirect("ver_carrito")

    request.session["carrito"] = {}
    request.session.modified = True

    messages.success(request, "El carrito está vacío.")

    return redirect("ver_carrito")
