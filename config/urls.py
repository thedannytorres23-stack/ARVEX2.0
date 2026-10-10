
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.core.views import home
from apps.catalog.views import detalle_producto

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path(
        "producto/<slug:slug>/",
        detalle_producto,
        name="detalle_producto"
    ),
   path("carrito/", include("apps.cart.urls")),

       path("pedidos/", include("apps.orders.urls")),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
