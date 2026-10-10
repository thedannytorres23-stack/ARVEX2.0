
from django.urls import path
from . import views

urlpatterns = [
    path(
        "finalizar/",
        views.finalizar_compra,
        name="finalizar_compra"
        
    ),
    path(
        "exito/<int:pedido_id>/",
        views.pedido_exitoso,
        name="pedido_exitoso"
    ),

    
]
