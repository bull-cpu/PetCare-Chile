from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import RegistroUsuarioForm, EditarPerfilForm
from .models import PerfilUsuario


def registro(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)

        if form.is_valid():
            usuario = form.save()
            messages.success(
                request,
                "Tu cuenta fue creada correctamente. ¡Bienvenido a PetCare Chile!"
            )
            login(request, usuario)
            return redirect("catalogo")
    else:
        form = RegistroUsuarioForm()

    return render(request, "usuarios/registro.html", {"form": form})


def iniciar_sesion(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            messages.success(request, "Has iniciado sesión correctamente.")
            return redirect("catalogo")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()

    return render(request, "usuarios/login.html", {"form": form})


@login_required
def cerrar_sesion(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Has cerrado sesión.")
        return redirect("catalogo")

    return redirect("catalogo")


@login_required
def editar_perfil(request):
    perfil, creado = PerfilUsuario.objects.get_or_create(
        usuario=request.user,
        defaults={
            "rut": "",
            "telefono": "",
            "rol": PerfilUsuario.Rol.CLIENTE,
        }
    )

    if request.method == "POST":
        form = EditarPerfilForm(request.POST, instance=perfil)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Tu perfil se actualizó correctamente."
            )
            return redirect("editar_perfil")
    else:
        form = EditarPerfilForm(instance=perfil)

    return render(
        request,
        "usuarios/editar_perfil.html",
        {"form": form}
    )