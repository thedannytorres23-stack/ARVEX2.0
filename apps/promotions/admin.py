
from django.contrib import admin
from .models import Cupon


@admin.register(Cupon)
class CuponAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "porcentaje",
        "activo",
        "fecha_vencimiento",
    )
    list_filter = ("activo",)
    search_fields = ("codigo",)
