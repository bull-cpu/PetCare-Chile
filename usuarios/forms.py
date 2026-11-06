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
            "username", "first_name", "last_name", "email",
            "rut", "telefono", "rol",
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


class EditarPerfilForm(forms.ModelForm):
    nombre = forms.CharField(
        max_length=150,
        label="Nombre",
        required=True
    )

    apellido = forms.CharField(
        max_length=150,
        label="Apellido",
        required=True
    )

    correo = forms.EmailField(
        label="Correo electrónico",
        required=True
    )

    class Meta:
        model = PerfilUsuario
        fields = ("rut", "telefono")
        labels = {
            "rut": "RUT",
            "telefono": "Teléfono",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields["nombre"].initial = self.instance.usuario.first_name
            self.fields["apellido"].initial = self.instance.usuario.last_name
            self.fields["correo"].initial = self.instance.usuario.email

    def clean_rut(self):
        rut = self.cleaned_data["rut"].strip()

        perfiles = PerfilUsuario.objects.filter(rut=rut).exclude(
            pk=self.instance.pk
        )

        if perfiles.exists():
            raise forms.ValidationError("Este RUT ya está registrado.")

        return rut

    def save(self, commit=True):
        perfil = super().save(commit=False)

        perfil.usuario.first_name = self.cleaned_data["nombre"]
        perfil.usuario.last_name = self.cleaned_data["apellido"]
        perfil.usuario.email = self.cleaned_data["correo"]

        if commit:
            perfil.usuario.save()
            perfil.save()

        return perfil