from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from inventario.models import Producto, Categoria
from inventario.serializers import ProductoSerializer, CategoriaSerializer, ProductoPostSerializer

# Create your views here.


class InventarioListView(APIView):
    def get(self, request):
        data = Producto.objects.all()
        serializer = ProductoSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        print(request.data)
        serializer = ProductoPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class InventarioDetailView(APIView):
    def get(self, request, pk=None):
        try:
            data = Producto.objects.get(pk=pk)
            serializer = ProductoSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Producto.DoesNotExist:
            return Response(data={"message": "el producto no existe"},
                     status=status.HTTP_404_NOT_FOUND)
    def put(self, request):
        pass
    def patch(self, request):
        pass
    def delete(self, request):
        pass

class CategoriaListView(APIView):
    def get(self, request):
        data = Categoria.objects.all()
        serializer = CategoriaSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        print(request.data)
        serializer = CategoriaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CategoriaDetailView(APIView):
    def get(self, request, pk=None):
        try:
            data = Categoria.objects.get(pk=pk)
            serializer = CategoriaSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Categoria.DoesNotExist:
            return Response(data={"message": "la categoria no existe"},
                     status=status.HTTP_404_NOT_FOUND)
    def put(self, request):
        pass
    def patch(self, request):
        pass
    def delete(self, request):
        pass