
from django.shortcuts import render
from apps.catalog.models import Producto, Categoria


def home(request):
    productos = (
        Producto.objects
        .filter(activo=True)
        .select_related("marca", "categoria")
        .order_by("-destacado", "-fecha_creacion")[:8]
    )

    categorias = Categoria.objects.all()

    return render(request, "home.html", {
        "productos": productos,
        "categorias": categorias,
    })
