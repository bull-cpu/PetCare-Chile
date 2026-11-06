
from django.contrib import admin
from django.utils.html import format_html

from .models import CategoriaServicio, Servicio


@admin.register(CategoriaServicio)
class CategoriaServicioAdmin(admin.ModelAdmin):

    list_display = (
        "nombre",
        "activa",
        "cantidad_servicios",
    )

    list_filter = ("activa",)
    search_fields = ("nombre",)
    list_editable = ("activa",)
    ordering = ("nombre",)

    @admin.display(description="Cantidad de servicios")
    def cantidad_servicios(self, obj):
        return obj.servicios.count()


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):

    list_display = (
        "nombre",
        "codigo",
        "categoria",
        "precio",
        "estado",
        "activo",
        "vista_previa",
    )

    list_filter = (
        "categoria",
        "estado",
        "activo",
    )

    search_fields = (
        "nombre",
        "codigo",
        "descripcion",
        "categoria__nombre",
    )

    list_editable = (
        "precio",
        "estado",
        "activo",
    )

    prepopulated_fields = {
        "codigo": ("nombre",)
    }

    readonly_fields = (
        "fecha_creacion",
        "vista_previa",
    )

    list_per_page = 15

    fieldsets = (
        ("Información del servicio", {
            "fields": (
                "nombre",
                "codigo",
                "categoria",
                "descripcion",
            )
        }),
        ("Precio y disponibilidad", {
            "fields": (
                "precio",
                "estado",
                "activo",
            )
        }),
        ("Imagen", {
            "fields": (
                "imagen",
                "vista_previa",
            )
        }),
        ("Información del sistema", {
            "fields": ("fecha_creacion",)
        }),
    )

    @admin.display(description="Fotografía")
    def vista_previa(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" width="80" height="60" '
                'style="object-fit: cover; border-radius: 8px;" />',
                obj.imagen.url
            )

        return "Sin imagen"

    @admin.action(description="Activar servicios seleccionados")
    def activar_servicios(self, request, queryset):
        cantidad = queryset.update(activo=True)
        self.message_user(
            request,
            f"{cantidad} servicios activados correctamente."
        )

    @admin.action(description="Desactivar servicios seleccionados")
    def desactivar_servicios(self, request, queryset):
        cantidad = queryset.update(activo=False)
        self.message_user(
            request,
            f"{cantidad} servicios desactivados correctamente."
        )

    actions = (
        "activar_servicios",
        "desactivar_servicios",
    )
