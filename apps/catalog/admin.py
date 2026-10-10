from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Marca, Categoria, Producto


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre", "marca", "categoria",
        "precio", "stock", "destacado", "activo"
    )
    list_filter = ("marca", "categoria", "activo", "destacado")
    search_fields = ("nombre", "descripcion")
    prepopulated_fields = {"slug": ("nombre",)}

