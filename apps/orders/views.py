
from decimal import Decimal

from django.db import transaction
from django.db.models import F
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from apps.catalog.models import Producto
from apps.promotions.models import Cupon

from .forms import PedidoForm
from .models import Pedido, DetallePedido


@require_http_methods(["GET", "POST"])
def finalizar_compra(request):
    carrito = request.session.get("carrito", {})

    if not carrito:
        return redirect("ver_carrito")

    form = PedidoForm(request.POST or None)

    if request.method == "POST" and form.is_valid():

        with transaction.atomic():

            productos = {
                str(p.id): p
                for p in Producto.objects.select_for_update().filter(
                    id__in=carrito.keys(),
                    activo=True
                )
            }

            subtotal = Decimal("0.00")
            detalles = []

            for clave, cantidad in carrito.items():
                producto = productos.get(clave)

                if (
                    producto is None
                    or type(cantidad) is not int
                    or cantidad <= 0
                    or cantidad > producto.stock
                ):
                    form.add_error(
                        None,
                        "Hay productos sin disponibilidad. "
                        "Revisa tu carrito."
                    )
                    break

                subtotal += producto.precio * cantidad
                detalles.append((producto, cantidad))

            if not form.errors:

                # Validar el cupón nuevamente al comprar
                descuento = Decimal("0.00")
                codigo = request.session.get("cupon_codigo")

                if codigo:
                    cupon = Cupon.objects.filter(
                        codigo=codigo
                    ).first()

                    if cupon and cupon.es_valido():
                        descuento = (
                            subtotal
                            * Decimal(cupon.porcentaje)
                            / Decimal("100")
                        ).quantize(Decimal("0.01"))
                    else:
                        request.session.pop("cupon_codigo", None)
                        form.add_error(
                            None,
                            "El cupón ya no es válido. "
                            "Revisa tu carrito antes de continuar."
                        )

                if not form.errors:
                    total = subtotal - descuento

                    pedido = Pedido.objects.create(
                        nombre=form.cleaned_data["nombre"],
                        telefono=form.cleaned_data["telefono"],
                        direccion=form.cleaned_data["direccion"],
                        total=total
                    )

                    for producto, cantidad in detalles:
                        DetallePedido.objects.create(
                            pedido=pedido,
                            producto=producto,
                            cantidad=cantidad,
                            precio=producto.precio
                        )

                        Producto.objects.filter(
                            pk=producto.pk
                        ).update(
                            stock=F("stock") - cantidad
                        )

                    request.session["carrito"] = {}
                    request.session.pop("cupon_codigo", None)

                    return redirect(
                        "pedido_exitoso",
                        pedido_id=pedido.id
                    )

    return render(
        request,
        "orders/finalizar.html",
        {"form": form}
    )


def pedido_exitoso(request, pedido_id):
    return render(
        request,
        "orders/exito.html",
        {"pedido_id": pedido_id}
    )
