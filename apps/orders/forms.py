
from django import forms


class PedidoForm(forms.Form):
    nombre = forms.CharField(
        max_length=150,
        label="Nombre completo"
    )
    telefono = forms.CharField(
        max_length=20,
        label="Teléfono"
    )
    direccion = forms.CharField(
        label="Dirección de entrega",
        widget=forms.Textarea(attrs={"rows": 3})
    )
