from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Pedido, DetallePedido


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ("producto", "cantidad", "precio")
    can_delete = False


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "telefono",
        "total",
        "estado",
        "fecha",
    )
    list_filter = ("estado", "fecha")
    search_fields = ("nombre", "telefono")
    readonly_fields = ("nombre", "telefono", "direccion", "total", "fecha")
    inlines = [DetallePedidoInline]
