from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import models
from .models import Tour, TourCategory, Booking

User = get_user_model()

class TourCategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий туров"""
    
    class Meta:
        model = TourCategory
        fields = ['id', 'name']

class TourSerializer(serializers.ModelSerializer):
    """Сериализатор для туров"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    available_slots = serializers.SerializerMethodField()
    
    class Meta:
        model = Tour
        fields = [
            'id', 'title', 'description', 'category', 'category_name',
            'city', 'country', 'price', 'duration_hours', 'start_date', 'end_date',
            'max_people', 'available_slots', 'is_active', 'created_at'
        ]
        read_only_fields = ['created_at', 'available_slots', 'category_name']
    
    def get_available_slots(self, obj):
        """Подсчет доступных мест"""
        confirmed_bookings = obj.bookings.filter(status='confirmed').aggregate(
            total=models.Sum('people_count')
        )['total'] or 0
        return obj.max_people - confirmed_bookings

class BookingSerializer(serializers.ModelSerializer):
    """Сериализатор для бронирований"""
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    tour_title = serializers.CharField(source='tour.title', read_only=True)
    tour_price = serializers.DecimalField(source='tour.price', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'tour', 'tour_title', 'tour_price', 'user_name',
            'people_count', 'total_price', 'status', 'created_at'
        ]
        read_only_fields = ['user_name', 'tour_title', 'tour_price', 'total_price', 'created_at', 'status']
    
    def validate(self, data):
        """Валидация бронирования"""
        tour = data['tour']
        people_count = data['people_count']
        
        if not tour.is_active:
            raise serializers.ValidationError("Тур неактивен")
        
        # Проверка доступных мест
        confirmed_bookings = tour.bookings.filter(status='confirmed').aggregate(
            total=models.Sum('people_count')
        )['total'] or 0
        
        available_slots = tour.max_people - confirmed_bookings
        
        if people_count > available_slots:
            raise serializers.ValidationError(
                f"Недостаточно мест. Доступно: {available_slots}"
            )
        
        return data
    
    def create(self, validated_data):
        """Создание бронирования с автоматическим расчетом стоимости"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class BookingListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка бронирований"""
    tour_title = serializers.CharField(source='tour.title', read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'tour_title', 'people_count', 'total_price', 'status', 'created_at']
