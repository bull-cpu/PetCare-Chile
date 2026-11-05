from django.contrib import admin
from .models import PerfilUsuario


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = (
        "usuario",
        "rut",
        "telefono",
        "rol",
    )

    list_filter = ("rol",)

    search_fields = (
        "usuariousername",
        "usuarioemail",
        "rut",
        "telefono",
    )