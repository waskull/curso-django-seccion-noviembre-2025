from django.db import models
from inventario.models import BaseModel, Producto
# Create your models here.

class Compra(BaseModel):
    proveedor = models.CharField(max_length=150)
    total = models.DecimalField(decimal_places=2, default=0)

class CompraDetalle(BaseModel):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    precio = models.DecimalField(decimal_places=2, default=0.1)