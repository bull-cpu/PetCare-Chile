from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):

    class Rol(models.TextChoices):
        CLIENTE = "cliente", "Cliente"
        PROVEEDOR = "proveedor", "Proveedor"

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="perfil"
    )

    rut = models.CharField(
        max_length=12,
        unique=True
    )

    telefono = models.CharField(max_length=20)

    rol = models.CharField(
        max_length=15,
        choices=Rol.choices,
        default=Rol.CLIENTE
    )

    def __str__(self):
        return f"{self.usuario.username} - {self.get_rol_display()}"

    class Meta:
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuarios"