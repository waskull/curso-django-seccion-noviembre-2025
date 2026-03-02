from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from .serializers import UsuarioSerializer


class UsuarioViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = []
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.is_anonymous:
            user = User.objects.create_user(
                **serializer.validated_data,
                is_staff=False,
                is_superuser=False
            )

        elif request.user.is_staff or request.user.is_superuser:
            is_staff = request.data.get('is_staff', True)
            is_superuser = request.data.get('is_superuser', False)
            user = User.objects.create_user(
                **serializer.validated_data,
                is_staff=is_staff,
                is_superuser=is_superuser
            )

        else:
            user = User.objects.create_user(
                **serializer.validated_data,
                is_staff=False,
                is_superuser=False
            )

        return Response(
            UsuarioSerializer(user).data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, pk=None):
        return self._perform_update(request, partial=False, pk=pk)

    def partial_update(self, request, pk=None):
        return self._perform_update(request, partial=True, pk=pk)

    def _perform_update(self, request, pk, partial):
        datos = self.get_object()
        
        if not (request.user.is_staff or request.user.is_superuser) and request.user != datos:
            return Response(
                {"detail": "No tienes permiso para editar a este usuario."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(datos, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        is_staff = request.data.get('is_staff')
        is_superuser = request.data.get('is_superuser')
        password = request.data.get('password')

        user = serializer.save()

        if request.user.is_staff or request.user.is_superuser:
            if is_staff is not None:
                user.is_staff = is_staff
            if is_superuser is not None:
                user.is_superuser = is_superuser
        
        if password:
            user.set_password(password)
        
        user.save()

        return Response(UsuarioSerializer(user).data)
    
    def destroy(self, request, pk=None):
        datos = self.get_object()

        if not (request.user.is_staff or request.user.is_superuser) and request.user != datos:
            return Response(
                {"detail": "No tienes permiso para eliminar este usuario."},
                status=status.HTTP_403_FORBIDDEN
            )

        if datos.is_superuser and User.objects.filter(is_superuser=True).count() <= 1:
            return Response(
                {"detail": "No se puede eliminar al único superusuario del sistema."},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_destroy(datos)
        return Response(
            {"detail": "Usuario eliminado correctamente."},
            status=status.HTTP_204_NO_CONTENT
        )
