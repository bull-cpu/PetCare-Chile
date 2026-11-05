from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import PerfilUsuario


class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, label="Nombre")
    last_name = forms.CharField(max_length=150, label="Apellido")

    rut = forms.CharField(max_length=12, label="RUT")
    telefono = forms.CharField(max_length=20, label="Teléfono")

    rol = forms.ChoiceField(
        choices=PerfilUsuario.Rol.choices,
        label="Tipo de usuario"
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "rut",
            "telefono",
            "rol",
        )

    def clean_rut(self):
        rut = self.cleaned_data["rut"].strip()

        if PerfilUsuario.objects.filter(rut=rut).exists():
            raise forms.ValidationError("Este RUT ya está registrado.")

        return rut

    def save(self, commit=True):
        usuario = super().save(commit=False)

        usuario.email = self.cleaned_data["email"]
        usuario.first_name = self.cleaned_data["first_name"]
        usuario.last_name = self.cleaned_data["last_name"]

        if commit:
            usuario.save()

            PerfilUsuario.objects.create(
                usuario=usuario,
                rut=self.cleaned_data["rut"],
                telefono=self.cleaned_data["telefono"],
                rol=self.cleaned_data["rol"],
            )

        return usuario