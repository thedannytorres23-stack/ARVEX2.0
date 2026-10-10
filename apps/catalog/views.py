from django.shortcuts import render

# Create your views here.



from django.shortcuts import render, get_object_or_404
from .models import Producto


def detalle_producto(request, slug):
    producto = get_object_or_404(
        Producto.objects.select_related("marca", "categoria"),
        slug=slug,
        activo=True
    )

    relacionados = (
        Producto.objects
        .filter(categoria=producto.categoria, activo=True)
        .exclude(pk=producto.pk)[:4]
    )

    return render(request, "catalog/detalle.html", {
        "producto": producto,
        "relacionados": relacionados,
    })
