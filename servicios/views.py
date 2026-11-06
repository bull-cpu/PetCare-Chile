
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator

from .models import CategoriaServicio, Servicio


def catalogo(request):
    servicios = Servicio.objects.filter(
        activo=True,
        estado=Servicio.Estado.DISPONIBLE,
        categoria__activa=True
    ).select_related("categoria")

    # Buscador
    busqueda = request.GET.get("q", "")

    if busqueda:
        servicios = servicios.filter(
            Q(nombre__icontains=busqueda) |
            Q(descripcion__icontains=busqueda) |
            Q(codigo__icontains=busqueda)
        )

    # Filtro por categoría
    categoria_id = request.GET.get("categoria", "")

    if categoria_id:
        servicios = servicios.filter(categoria_id=categoria_id)

    # Ordenamiento
    orden = request.GET.get("orden", "nombre")

    if orden in ["nombre", "-nombre", "precio", "-precio"]:
        servicios = servicios.order_by(orden)
    else:
        servicios = servicios.order_by("nombre")

    # Paginación
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
