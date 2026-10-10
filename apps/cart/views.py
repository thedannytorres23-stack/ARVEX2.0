from django.shortcuts import render

# Create your views here.



from decimal import Decimal

from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.catalog.models import Producto


def obtener_carrito(request):
    return request.session.get("carrito", {})


@require_POST
def agregar_carrito(request, producto_id):
    producto = get_object_or_404(
        Producto, id=producto_id, activo=True
    )

    carrito = obtener_carrito(request)
    clave = str(producto.id)
    cantidad = carrito.get(clave, 0)

    if cantidad < producto.stock:
        carrito[clave] = cantidad + 1
        request.session["carrito"] = carrito

    return redirect("ver_carrito")


def ver_carrito(request):
    carrito = obtener_carrito(request)
    productos = Producto.objects.filter(
        id__in=carrito.keys(), activo=True
    )

    items = []
    total = Decimal("0.00")

    for producto in productos:
        cantidad = carrito[str(producto.id)]
        subtotal = producto.precio * cantidad
        total += subtotal

        items.append({
            "producto": producto,
            "cantidad": cantidad,
            "subtotal": subtotal,
        })

    return render(request, "cart/carrito.html", {
        "items": items,
        "total": total,
    })


@require_POST
def eliminar_carrito(request, producto_id):
    carrito = obtener_carrito(request)
    clave = str(producto_id)

    if clave in carrito:
        del carrito[clave]
        request.session["carrito"] = carrito

    return redirect("ver_carrito")


@require_POST
def actualizar_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    carrito = obtener_carrito(request)
    clave = str(producto_id)

    if clave in carrito:
        try:
            cantidad = int(request.POST.get("cantidad", 1))
        except (TypeError, ValueError):
            cantidad = 1

        if cantidad <= 0:
            del carrito[clave]
        else:
            carrito[clave] = min(cantidad, producto.stock)

        request.session["carrito"] = carrito

    return redirect("ver_carrito")
