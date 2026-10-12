
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Sum

from apps.catalog.models import Producto
from .models import MovimientoInventario


@staff_member_required(login_url="/admin/login/")
def panel_almacen(request):
    productos = Producto.objects.select_related(
        "marca", "categoria"
    ).order_by("nombre")

    movimientos = MovimientoInventario.objects.select_related(
        "producto"
    ).order_by("-fecha")[:15]

    total_productos = productos.count()
    total_unidades = productos.aggregate(
        total=Sum("stock")
    )["total"] or 0

    stock_bajo = productos.filter(stock__lte=5).count()

    return render(request, "warehouse/panel.html", {
        "productos": productos,
        "movimientos": movimientos,
        "total_productos": total_productos,
        "total_unidades": total_unidades,
        "stock_bajo": stock_bajo,
    })
