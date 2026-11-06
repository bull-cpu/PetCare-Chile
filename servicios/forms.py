from django import forms

from .models import Servicio


class ServicioForm(forms.ModelForm):

    class Meta:
        model = Servicio

        fields = [
            "categoria",
            "codigo",
            "nombre",
            "descripcion",
            "precio",
            "estado",
            "imagen",
            "activo",
        ]

        widgets = {
            "categoria": forms.Select(
                attrs={"class": "form-select"}
            ),
            "codigo": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "nombre": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4
                }
            ),
            "precio": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.01"
                }
            ),
            "estado": forms.Select(
                attrs={"class": "form-select"}
            ),
            "imagen": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "activo": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }

    def clean_precio(self):
        precio = self.cleaned_data["precio"]

        if precio < 0:
            raise forms.ValidationError(
                "El precio no puede ser negativo."
            )

        return precio

    def clean_codigo(self):
        codigo = self.cleaned_data["codigo"].strip()

        if not codigo:
            raise forms.ValidationError(
                "El código del servicio es obligatorio."
            )

        return codigo