
from django.urls import path
from . import views

urlpatterns = [
    path("", views.ver_carrito, name="ver_carrito"),
    path("agregar/<int:producto_id>/", views.agregar_carrito, name="agregar_carrito"),
    path("actualizar/<int:producto_id>/", views.actualizar_carrito, name="actualizar_carrito"),
    path("eliminar/<int:producto_id>/", views.eliminar_carrito, name="eliminar_carrito"),
]
