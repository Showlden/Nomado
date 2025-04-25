from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label="Пароль"
    )
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'role', 'access', 'refresh')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        refresh = RefreshToken.for_user(user)
        self._access = str(refresh.access_token)
        self._refresh = str(refresh)
        return user

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['access'] = self._access
        rep['refresh'] = self._refresh
        return rep


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, label="Email")
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label="Пароль"
    )

    def validate(self, data):
        from django.contrib.auth import authenticate
        user = authenticate(email=data['email'], password=data['password'])
        
        if not user:
            raise serializers.ValidationError("Неверный email или пароль")
        if not user.is_active:
            raise serializers.ValidationError("Пользователь деактивирован")
            
        refresh = RefreshToken.for_user(user)
        return {
            'user': user.email,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }