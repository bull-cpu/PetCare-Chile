
from django.contrib import admin
from .models import CategoriaServicio, Servicio


@admin.register(CategoriaServicio)
class CategoriaServicioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activa")
    list_filter = ("activa",)
    search_fields = ("nombre",)
    list_editable = ("activa",)


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "categoria",
        "precio",
        "estado",
        "activo",
    )
    list_filter = ("categoria", "estado", "activo")
    search_fields = ("nombre", "codigo", "descripcion")
    list_editable = ("estado", "activo")
    prepopulated_fields = {"codigo": ("nombre",)}

    fieldsets = (
        ("Información del servicio", {
            "fields": ("nombre", "codigo", "categoria", "descripcion")
        }),
        ("Precio y disponibilidad", {
            "fields": ("precio", "estado", "activo")
        }),
        ("Imagen", {
            "fields": ("imagen",)
        }),
    )
