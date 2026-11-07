
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse

from .models import CategoriaServicio, Servicio
from .context_processors import resumen_carrito


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


class CRUDServiciosTests(TestCase):

    def setUp(self):
        self.categoria = CategoriaServicio.objects.create(
            nombre="Veterinaria",
            descripcion="Servicios veterinarios",
            activa=True
        )

        self.servicio = Servicio.objects.create(
            categoria=self.categoria,
            codigo="consulta-prueba",
            nombre="Consulta de prueba",
            descripcion="Servicio para pruebas CRUD",
            precio=15000,
            estado=Servicio.Estado.DISPONIBLE,
            activo=True
        )

        self.admin = User.objects.create_user(
            username="administrador",
            password="ClavePrueba123",
            is_staff=True
        )

    def test_administracion_requiere_inicio_sesion(self):
        respuesta = self.client.get(
            reverse("administrar_servicios")
        )
        self.assertEqual(respuesta.status_code, 302)

    def test_administrador_puede_ver_servicios(self):
        self.client.force_login(self.admin)

        respuesta = self.client.get(
            reverse("administrar_servicios")
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Consulta de prueba")

    def test_administrador_puede_crear_servicio(self):
        self.client.force_login(self.admin)

        respuesta = self.client.post(
            reverse("crear_servicio"),
            {
                "categoria": self.categoria.id,
                "codigo": "nuevo-servicio",
                "nombre": "Nuevo servicio",
                "descripcion": "Descripción del servicio",
                "precio": "20000",
                "estado": Servicio.Estado.DISPONIBLE,
                "activo": "on",
            }
        )

        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(
            Servicio.objects.filter(codigo="nuevo-servicio").exists()
        )

    def test_administrador_puede_editar_servicio(self):
        self.client.force_login(self.admin)

        respuesta = self.client.post(
            reverse(
                "editar_servicio",
                args=[self.servicio.id]
            ),
            {
                "categoria": self.categoria.id,
                "codigo": "consulta-prueba",
                "nombre": "Servicio actualizado",
                "descripcion": "Descripción actualizada",
                "precio": "18000",
                "estado": Servicio.Estado.DISPONIBLE,
                "activo": "on",
            }
        )

        self.assertEqual(respuesta.status_code, 302)

        self.servicio.refresh_from_db()
        self.assertEqual(self.servicio.nombre, "Servicio actualizado")
        self.assertEqual(self.servicio.precio, 18000)

    def test_administrador_puede_desactivar_servicio(self):
        self.client.force_login(self.admin)

        respuesta = self.client.post(
            reverse(
                "eliminar_servicio",
                args=[self.servicio.id]
            )
        )

        self.assertEqual(respuesta.status_code, 302)

        self.servicio.refresh_from_db()
        self.assertFalse(self.servicio.activo)


class ResumenCarritoTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.categoria = CategoriaServicio.objects.create(
            nombre="Veterinaria",
            descripcion="Servicios veterinarios",
            activa=True
        )

        self.servicio = Servicio.objects.create(
            categoria=self.categoria,
            codigo="resumen-prueba",
            nombre="Servicio de prueba",
            descripcion="Servicio para probar el resumen",
            precio=15000,
            estado=Servicio.Estado.DISPONIBLE,
            activo=True
        )

    def crear_request(self, carrito=None):
        request = self.factory.get("/")
        middleware = SessionMiddleware(lambda request: None)
        middleware.process_request(request)
        request.session.save()
        request.session["carrito"] = carrito or {}
        return request

    def test_carrito_vacio(self):
        resultado = resumen_carrito(self.crear_request())

        self.assertEqual(resultado["carrito_resumen"], [])
        self.assertEqual(resultado["carrito_cantidad"], 0)
        self.assertEqual(resultado["carrito_total"], Decimal("0.00"))

    def test_calcula_cantidad_y_total(self):
        request = self.crear_request({
            str(self.servicio.id): 2
        })

        resultado = resumen_carrito(request)

        self.assertEqual(resultado["carrito_cantidad"], 2)
        self.assertEqual(resultado["carrito_total"], Decimal("30000.00"))
        self.assertEqual(len(resultado["carrito_resumen"]), 1)

    def test_excluye_servicios_inactivos(self):
        self.servicio.activo = False
        self.servicio.save()

        request = self.crear_request({
            str(self.servicio.id): 2
        })

        resultado = resumen_carrito(request)

        self.assertEqual(resultado["carrito_resumen"], [])
        self.assertEqual(resultado["carrito_cantidad"], 0)
        self.assertEqual(resultado["carrito_total"], Decimal("0.00"))
