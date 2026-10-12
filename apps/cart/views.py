
from decimal import Decimal

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.catalog.models import Producto
from apps.promotions.models import Cupon


# ==========================================
# OBTENER CARRITO
# ==========================================

def obtener_carrito(request):
    return request.session.get("carrito", {})


# ==========================================
# CALCULAR DESCUENTOS
# ==========================================

def calcular_descuento(request, subtotal):
    codigo = request.session.get("cupon_codigo")
    cupon = None
    descuento = Decimal("0.00")

    if codigo:
        cupon = Cupon.objects.filter(codigo=codigo).first()

        if cupon and cupon.es_valido():
            descuento = (
                subtotal
                * Decimal(cupon.porcentaje)
                / Decimal("100")
            ).quantize(Decimal("0.01"))
        else:
            request.session.pop("cupon_codigo", None)
            cupon = None

    return cupon, descuento


# ==========================================
# AGREGAR PRODUCTO AL CARRITO
# ==========================================

@require_POST
def agregar_carrito(request, producto_id):
    producto = get_object_or_404(
        Producto,
        id=producto_id,
        activo=True
    )

    carrito = obtener_carrito(request)
    clave = str(producto.id)
    cantidad = carrito.get(clave, 0)

    if cantidad < producto.stock:
        carrito[clave] = cantidad + 1
        request.session["carrito"] = carrito

        messages.success(
            request,
            f"{producto.nombre} agregado al carrito."
        )
    else:
        messages.warning(
            request,
            "No hay más unidades disponibles de este producto."
        )

    return redirect("ver_carrito")


# ==========================================
# VER CARRITO
# ==========================================

def ver_carrito(request):
    carrito = obtener_carrito(request)

    productos = Producto.objects.filter(
        id__in=carrito.keys(),
        activo=True
    ).select_related("marca")

    items = []
    subtotal = Decimal("0.00")

    for producto in productos:
        cantidad = carrito[str(producto.id)]

        total_producto = producto.precio * cantidad
        subtotal += total_producto

        items.append({
            "producto": producto,
            "cantidad": cantidad,
            "subtotal": total_producto,
        })

    # Aplicar descuentos después de sumar los productos
    cupon, descuento = calcular_descuento(
        request,
        subtotal
    )

    total_final = subtotal - descuento

    return render(
        request,
        "cart/carrito.html",
        {
            "items": items,
            "subtotal": subtotal,
            "cupon": cupon,
            "descuento": descuento,
            "total": total_final,
        }
    )


# ==========================================
# ACTUALIZAR CANTIDAD
# ==========================================

@require_POST
def actualizar_carrito(request, producto_id):
    producto = get_object_or_404(
        Producto,
        id=producto_id,
        activo=True
    )

    carrito = obtener_carrito(request)
    clave = str(producto_id)

    if clave in carrito:
        try:
            cantidad = int(
                request.POST.get("cantidad", 1)
            )
        except (TypeError, ValueError):
            cantidad = 1

        if cantidad <= 0:
            del carrito[clave]

            messages.info(
                request,
                "Producto eliminado del carrito."
            )
        else:
            cantidad_final = min(
                cantidad,
                producto.stock
            )

            if cantidad_final == 0:
                del carrito[clave]
                messages.warning(
                    request,
                    "Producto eliminado porque no tiene stock."
                )
            else:
                carrito[clave] = cantidad_final

                if cantidad_final < cantidad:
                    messages.warning(
                        request,
                        "La cantidad se ajustó al stock disponible."
                    )
                else:
                    messages.success(
                        request,
                        "Cantidad actualizada correctamente."
                    )

        request.session["carrito"] = carrito

    return redirect("ver_carrito")


# ==========================================
# ELIMINAR PRODUCTO
# ==========================================

@require_POST
def eliminar_carrito(request, producto_id):
    carrito = obtener_carrito(request)
    clave = str(producto_id)

    if clave in carrito:
        del carrito[clave]
        request.session["carrito"] = carrito

        messages.success(
            request,
            "Producto eliminado del carrito."
        )

    return redirect("ver_carrito")


# ==========================================
# APLICAR CUPÓN
# ==========================================

@require_POST
def aplicar_cupon(request):
    codigo = request.POST.get(
        "codigo", ""
    ).strip().upper()

    if not obtener_carrito(request):
        messages.warning(
            request,
            "Agrega productos antes de aplicar un cupón."
        )
        return redirect("ver_carrito")

    cupon = Cupon.objects.filter(
        codigo=codigo
    ).first()

    if cupon and cupon.es_valido():
        request.session["cupon_codigo"] = cupon.codigo

        messages.success(
            request,
            f"¡Cupón {cupon.codigo} aplicado! "
            f"Obtienes un {cupon.porcentaje}% de descuento."
        )
    else:
        request.session.pop("cupon_codigo", None)

        messages.error(
            request,
            "El cupón no existe, está desactivado o ha vencido."
        )

    return redirect("ver_carrito")


# ==========================================
# QUITAR CUPÓN
# ==========================================

@require_POST
def quitar_cupon(request):
    request.session.pop("cupon_codigo", None)

    messages.info(
        request,
        "Cupón eliminado correctamente."
    )

    return redirect("ver_carrito")
