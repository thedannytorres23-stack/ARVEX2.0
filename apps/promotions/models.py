
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Cupon(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    porcentaje = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )
    activo = models.BooleanField(default=True)
    fecha_vencimiento = models.DateTimeField()

    def es_valido(self):
        return self.activo and self.fecha_vencimiento > timezone.now()

    def save(self, *args, **kwargs):
        self.codigo = self.codigo.strip().upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo} - {self.porcentaje}%"
