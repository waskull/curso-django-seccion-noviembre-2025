from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Categoria, Producto

# Create your views here.


class ProductListView(APIView):
    def get(self, request):
        data = []
        for producto in Producto.objects.all():
            data.append({
                "id": producto.id,
                "nombre": producto.nombre,
                "cantidad": producto.cantidad,
                "descripcion": producto.descripcion,
                "categoria": producto.categoria.nombre
            })
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            formData = request.data.copy()
            id_cat = request.data["categoria"]
            formData.pop("categoria")
            categoria = Categoria.objects.get(id=id_cat)

            exists = Producto.objects.filter(nombre=formData["nombre"]).exists()
            if exists:
                return Response(data={"message": "El producto ya existe"}, status=status.HTTP_400_BAD_REQUEST)

            Producto.objects.create(**formData, categoria=categoria)
            return Response(data={"message": "Producto creado"}, status=status.HTTP_200_OK)
        except Categoria.DoesNotExist:
            return Response(data={"message": "No se encontro la categoria"}, status=status.HTTP_404_NOT_FOUND)

class ProductDetailView(APIView):
    def get(self, request, pk=None):
        data = Producto.objects.filter(id=pk).first()
        if not data:
            return Response(data={"message": "No se encontro el producto"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "id": data.id,
            "nombre": data.nombre,
            "cantidad": data.cantidad,
            "descripcion": data.descripcion,
            "categoria": data.categoria.nombre
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        try:
            data = Producto.objects.get(id=pk).delete()
            return Response(data={"message": f"El producto {data.nombre} ha sido eliminado"}, status=status.HTTP_200_OK)
        except Producto.DoesNotExist:
            return Response(data={"message": "No se encontro el producto"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk=None):
        pass

    def patch(self, request, pk=None):
        try:
            data = Producto.objects.filter(id=pk).first()
            nombre = request.data.get("nombre", data.nombre)
            Producto.objects.filter(id=pk).update(nombre=nombre)
            return Response(data={"message": f"El producto {nombre} ha sido actualizado"}, status=status.HTTP_200_OK)
        except Producto.DoesNotExist:
            return Response(data={"message": "No se encontro el producto"}, status=status.HTTP_404_NOT_FOUND)

class ProductViewSet(ViewSet):
    def list(self, request):
        data = [
            {
                "id": producto.id,
                "nombre": producto.nombre,
                "cantidad": producto.cantidad,
                "descripcion": producto.descripcion,
                "categoria": producto.categoria.nombre
            } for producto in Producto.objects.all()
        ]
        return Response(data=data, status=status.HTTP_200_OK)

    def create(self, request):
        try:
            formData = request.data.copy()
            id_cat = request.data["categoria"]
            formData.pop("categoria")
            categoria = Categoria.objects.get(id=id_cat)

            exists = Producto.objects.filter(nombre=formData["nombre"]).exists()
            if exists:
                return Response(data={"message": "El producto ya existe"}, status=status.HTTP_400_BAD_REQUEST)

            Producto.objects.create(**formData, categoria=categoria)
            return Response(data={"message": "Producto creado"}, status=status.HTTP_200_OK)
        except Categoria.DoesNotExist:
            return Response(data={"message": "No se encontro la categoria"}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        data = Producto.objects.filter(id=pk).first()
        if not data:
            return Response(data={"message": "No se encontro el producto"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "id": data.id,
            "nombre": data.nombre,
            "cantidad": data.cantidad,
            "descripcion": data.descripcion,
            "categoria": data.categoria.nombre
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        try:
            formData = request.data.copy()
            cat_id = request.data["categoria"]
            formData.pop("categoria")
            categoria = Categoria.objects.get(id=cat_id)
            Producto.objects.filter(id=pk).update(**formData, categoria=categoria)
            return Response(data={"message": f"El producto {formData['nombre']} ha sido actualizado"}, status=status.HTTP_200_OK)
        except Producto.DoesNotExist:
            return Response(data={"message": "No se encontro el producto"}, status=status.HTTP_404_NOT_FOUND)
        except Categoria.DoesNotExist:
            return Response(data={"message": "No se encontro la categoria"}, status=status.HTTP_404_NOT_FOUND)


    def partial_update(self, request, pk=None):
        try:
            data = Producto.objects.filter(id=pk).first()
            nombre = request.data.get("nombre", data.nombre)
            Producto.objects.filter(id=pk).update(nombre=nombre)
            return Response(data={"message": f"El producto {nombre} ha sido actualizado"}, status=status.HTTP_200_OK)
        except Producto.DoesNotExist:
            return Response(data={"message": "No se encontro el producto"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            Producto.objects.get(id=pk).delete()
            return Response(data={"message": f"El producto ha sido eliminado"}, status=status.HTTP_200_OK)
        except Producto.DoesNotExist:
            return Response(data={"message": "No se encontro el producto"}, status=status.HTTP_404_NOT_FOUND)
