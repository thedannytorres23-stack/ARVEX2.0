
from django.db import models
from django.core.exceptions import ValidationError
from django.db import transaction
from apps.catalog.models import Producto


class MovimientoInventario(models.Model):
    TIPOS = [
        ("entrada", "Entrada de mercancía"),
        ("salida", "Salida de mercancía"),
    ]

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name="movimientos"
    )
    tipo = models.CharField(max_length=10, choices=TIPOS)
    cantidad = models.PositiveIntegerField()
    motivo = models.CharField(max_length=200)
    fecha = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.cantidad is None or self.cantidad <= 0:
            raise ValidationError({
                "cantidad": "La cantidad debe ser mayor que cero."
            })

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError(
                "Los movimientos registrados no se pueden editar."
            )

        self.full_clean()

        with transaction.atomic():
            producto = Producto.objects.select_for_update().get(
                pk=self.producto_id
            )

            if self.tipo == "entrada":
                producto.stock += self.cantidad
            else:
                if producto.stock < self.cantidad:
                    raise ValidationError(
                        "No hay suficiente stock para esta salida."
                    )
                producto.stock -= self.cantidad

            producto.save(update_fields=["stock"])
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.producto.nombre}"
