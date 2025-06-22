from rest_framework import generics, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import OpenApiResponse
from .serializers import RegisterSerializer, LoginSerializer

class RegisterView(generics.CreateAPIView):
    """Регистрация нового пользователя"""
    serializer_class = RegisterSerializer
    
    @extend_schema(
        summary="Регистрация пользователя",
        description="Создает новый аккаунт пользователя",
        responses={
            201: RegisterSerializer,
            400: OpenApiResponse(description="Ошибка валидации данных")
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    """Вход в систему"""
    serializer_class = LoginSerializer
    
    @extend_schema(
        summary="Вход в систему",
        description="Аутентификация пользователя и получение JWT токенов",
        responses={
            200: LoginSerializer,
            400: OpenApiResponse(description="Неверные учетные данные")
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
