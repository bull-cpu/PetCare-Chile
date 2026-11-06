
from django.test import TestCase
from django.urls import reverse

from .models import CategoriaServicio, Servicio


class CatalogoTests(TestCase):

    def setUp(self):
        self.categoria = CategoriaServicio.objects.create(
            nombre="Veterinaria",
            descripcion="Servicios veterinarios",
            activa=True
        )

        self.servicio = Servicio.objects.create(
            categoria=self.categoria,
            codigo="consulta-veterinaria",
            nombre="Consulta veterinaria",
            descripcion="Atención médica para mascotas",
            precio=15000,
            estado=Servicio.Estado.DISPONIBLE,
            activo=True
        )

    def test_catalogo_muestra_servicios_activos(self):
        respuesta = self.client.get(reverse("catalogo"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Consulta veterinaria")

    def test_busqueda_por_nombre(self):
        respuesta = self.client.get(
            reverse("catalogo"),
            {"q": "Consulta veterinaria"}
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Consulta veterinaria")

    def test_filtro_por_categoria(self):
        respuesta = self.client.get(
            reverse("catalogo"),
            {"categoria": self.categoria.id}
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Consulta veterinaria")

    def test_detalle_servicio(self):
        respuesta = self.client.get(
            reverse("detalle_servicio", kwargs={
                "codigo": self.servicio.codigo
            })
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Consulta veterinaria")

    def test_servicio_inactivo_no_aparece_en_catalogo(self):
        self.servicio.activo = False
        self.servicio.save()

        respuesta = self.client.get(reverse("catalogo"))
        self.assertNotContains(respuesta, "Consulta veterinaria")

    def test_detalle_servicio_inactivo_devuelve_404(self):
        self.servicio.activo = False
        self.servicio.save()

        respuesta = self.client.get(
            reverse("detalle_servicio", kwargs={
                "codigo": self.servicio.codigo
            })
        )
        self.assertEqual(respuesta.status_code, 404)

    def test_servicio_no_disponible_no_aparece(self):
        self.servicio.estado = Servicio.Estado.AGOTADO
        self.servicio.save()

        respuesta = self.client.get(reverse("catalogo"))
        self.assertNotContains(respuesta, "Consulta veterinaria")

    def test_detalle_servicio_no_disponible_devuelve_404(self):
        self.servicio.estado = Servicio.Estado.AGOTADO
        self.servicio.save()

        respuesta = self.client.get(
            reverse("detalle_servicio", kwargs={
                "codigo": self.servicio.codigo
            })
        )
        self.assertEqual(respuesta.status_code, 404)

    def test_categoria_inactiva_no_muestra_servicios(self):
        self.categoria.activa = False
        self.categoria.save()

        respuesta = self.client.get(reverse("catalogo"))
        self.assertNotContains(respuesta, "Consulta veterinaria")


class CarritoTests(TestCase):

    def setUp(self):
        self.categoria = CategoriaServicio.objects.create(
            nombre="Veterinaria",
            descripcion="Servicios veterinarios",
            activa=True
        )

        self.servicio = Servicio.objects.create(
            categoria=self.categoria,
            codigo="consulta-veterinaria",
            nombre="Consulta veterinaria",
            descripcion="Atención médica para mascotas",
            precio=15000,
            estado=Servicio.Estado.DISPONIBLE,
            activo=True
        )

    def test_agregar_servicio_al_carrito(self):
        respuesta = self.client.post(
            reverse("agregar_carrito", kwargs={
                "servicio_id": self.servicio.id
            })
        )

        self.assertRedirects(respuesta, reverse("ver_carrito"))

        carrito = self.client.session["carrito"]
        self.assertEqual(carrito[str(self.servicio.id)], 1)

    def test_agregar_mismo_servicio_aumenta_cantidad(self):
        url = reverse("agregar_carrito", kwargs={
            "servicio_id": self.servicio.id
        })

        self.client.post(url)
        self.client.post(url)

        carrito = self.client.session["carrito"]
        self.assertEqual(carrito[str(self.servicio.id)], 2)

    def test_actualizar_cantidad_del_carrito(self):
        self.client.post(
            reverse("agregar_carrito", kwargs={
                "servicio_id": self.servicio.id
            })
        )

        respuesta = self.client.post(
            reverse("actualizar_carrito", kwargs={
                "servicio_id": self.servicio.id
            }),
            {"cantidad": 3}
        )

        self.assertRedirects(respuesta, reverse("ver_carrito"))

        carrito = self.client.session["carrito"]
        self.assertEqual(carrito[str(self.servicio.id)], 3)

    def test_eliminar_servicio_del_carrito(self):
        self.client.post(
            reverse("agregar_carrito", kwargs={
                "servicio_id": self.servicio.id
            })
        )

        self.client.post(
            reverse("eliminar_carrito", kwargs={
                "servicio_id": self.servicio.id
            })
        )

        carrito = self.client.session["carrito"]
        self.assertNotIn(str(self.servicio.id), carrito)

    def test_vaciar_carrito(self):
        self.client.post(
            reverse("agregar_carrito", kwargs={
                "servicio_id": self.servicio.id
            })
        )

        respuesta = self.client.post(reverse("vaciar_carrito"))

        self.assertRedirects(respuesta, reverse("ver_carrito"))
        self.assertEqual(self.client.session["carrito"], {})

    def test_no_se_puede_agregar_servicio_inactivo(self):
        self.servicio.activo = False
        self.servicio.save()

        respuesta = self.client.post(
            reverse("agregar_carrito", kwargs={
                "servicio_id": self.servicio.id
            })
        )

        self.assertEqual(respuesta.status_code, 404)
        self.assertNotIn("carrito", self.client.session)