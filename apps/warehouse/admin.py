
from django.contrib import admin
from .models import MovimientoInventario


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = (
        "producto",
        "tipo",
        "cantidad",
        "motivo",
        "fecha",
    )

    list_filter = ("tipo", "fecha")
    search_fields = ("producto__nombre", "motivo")
    readonly_fields = ("fecha",)

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False
