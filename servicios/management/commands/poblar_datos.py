
from django.core.management.base import BaseCommand
from servicios.models import CategoriaServicio, Servicio


class Command(BaseCommand):
    help = "Carga categorías y servicios de prueba para PetCare Chile"

    def handle(self, *args, **kwargs):

        categorias = [
            ("Veterinaria", "Consultas y atención médica para mascotas"),
            ("Peluquería", "Baños, cortes y cuidados estéticos"),
            ("Hospedaje", "Alojamiento y cuidado temporal"),
            ("Paseos", "Paseos y actividad física para mascotas"),
        ]

        categorias_creadas = {}

        for nombre, descripcion in categorias:
            categoria, creada = CategoriaServicio.objects.get_or_create(
                nombre=nombre,
                defaults={"descripcion": descripcion}
            )
            categorias_creadas[nombre] = categoria

        servicios = [
            ("consulta-veterinaria", "Consulta veterinaria general",
             "Atención veterinaria general para mascotas", 15000, "Veterinaria"),
            ("vacunacion", "Vacunación de mascotas",
             "Aplicación de vacunas para perros y gatos", 12000, "Veterinaria"),
            ("control-salud", "Control de salud",
             "Evaluación preventiva de salud", 10000, "Veterinaria"),
            ("bano-mascota", "Baño de mascotas",
             "Servicio de baño y limpieza", 10000, "Peluquería"),
            ("corte-pelo", "Corte de pelo",
             "Corte y arreglo de pelaje", 15000, "Peluquería"),
            ("hospedaje-diario", "Hospedaje diario",
             "Alojamiento temporal para mascotas", 20000, "Hospedaje"),
            ("paseo-30-min", "Paseo de 30 minutos",
             "Paseo individual para mascotas", 8000, "Paseos"),
            ("paseo-60-min", "Paseo de 60 minutos",
             "Paseo extendido para mascotas", 12000, "Paseos"),
        ]

        for codigo, nombre, descripcion, precio, categoria_nombre in servicios:
            Servicio.objects.update_or_create(
                codigo=codigo,
                defaults={
                    "nombre": nombre,
                    "descripcion": descripcion,
                    "precio": precio,
                    "categoria": categorias_creadas[categoria_nombre],
                    "estado": Servicio.Estado.DISPONIBLE,
                    "activo": True,
                }
            )

        self.stdout.write(
            self.style.SUCCESS(
                "PetCare Chile: categorías y 8 servicios cargados correctamente."
            )
        )
