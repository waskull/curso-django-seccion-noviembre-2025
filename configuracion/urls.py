
from django.contrib import admin
from django.urls import path
from inventario.views import InventarioListView, InventarioDetailView, CategoriaListView, CategoriaDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/categoria/', CategoriaListView.as_view(), name="categoria"),
    path('api/categoria/<int:pk>/', CategoriaDetailView.as_view(), name="categoria-detalle"),
    path('api/inventario/', InventarioListView.as_view(), name="inventario"),
    path('api/inventario/<int:pk>/', InventarioDetailView.as_view(), name="inventario-detalle")
]
