from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inventario.views import ProductListView, ProductDetailView, ProductViewSet

router = DefaultRouter()
router.register(r'inventarioo', ProductViewSet, basename='inventarioo')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/inventario/', ProductListView.as_view(), name='inventario'),
    path('api/inventario/<int:pk>/', ProductDetailView.as_view(), name='inventario-detalle'),
    path('api/', include(router.urls)),
]
