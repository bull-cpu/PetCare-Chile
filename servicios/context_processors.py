
from decimal import Decimal

from .models import Servicio


def resumen_carrito(request):
    carrito = request.session.get("carrito", {})

    servicios_ids = [
        int(servicio_id)
        for servicio_id in carrito
        if str(servicio_id).isdigit()
    ]

    servicios = Servicio.objects.filter(
        id__in=servicios_ids,
        activo=True,
        estado=Servicio.Estado.DISPONIBLE,
        categoria__activa=True
    ).select_related("categoria")

    resumen = []
    cantidad_total = 0
    total = Decimal("0.00")

    for servicio in servicios:
        cantidad = carrito.get(str(servicio.id), 0)

        if not isinstance(cantidad, int) or cantidad <= 0:
            continue

        subtotal = servicio.precio * cantidad

        resumen.append({
            "servicio": servicio,
            "cantidad": cantidad,
            "subtotal": subtotal,
        })

        cantidad_total += cantidad
        total += subtotal

    return {
        "carrito_resumen": resumen,
        "carrito_cantidad": cantidad_total,
        "carrito_total": total,
    }
