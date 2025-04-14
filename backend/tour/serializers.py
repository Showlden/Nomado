from django.contrib.auth import get_user_model

from rest_framework import serializers
from .models import Tour, TourCategory, Location, Booking, Review, Favorite

User = get_user_model()

class TourCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourCategory
        fields = ['id', 'name', 'description']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'country', 'city', 'image']

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    tour = serializers.StringRelatedField(read_only=True)
    tour_id = serializers.PrimaryKeyRelatedField(
        queryset=Tour.objects.all(), write_only=True, source='tour'
    )

    class Meta:
        model = Booking
        fields = [
            'id',
            'user',
            'tour',
            'tour_id',
            'number_of_people',
            'booking_date',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'tour', 'status', 'created_at', 'updated_at']




class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = [
            'id', 'title', 'description', 'price', 'duration',
            'category', 'location', 'guide', 'image', 'start_datetime',
            'end_datetime', 'max_people', 'available_slots'
        ]
        read_only_fields = ('guide', 'available_slots')
    
    def get_bookings(self, obj):
        related_bookings = obj.bookings.all()  
        return BookingSerializer(related_bookings, many=True).data

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    tour = serializers.SerializerMethodField(read_only=True)
    tour_id = serializers.PrimaryKeyRelatedField(
        queryset=Tour.objects.all(), write_only=True, source='tour'
    )

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'tour',
            'tour_id',
            'rating',
            'comment',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_tour(self, obj):
        return obj.tour.title if obj.tour else None

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate(self, data):
        request = self.context['request']
        user = request.user
        tour = data.get('tour')

        # Если обновляем — игнорируем текущий объект
        if request.method in ['PUT', 'PATCH']:
            instance = self.instance
            if instance and instance.tour == tour and instance.user == user:
                return data

        if Review.objects.filter(user=user, tour=tour).exists():
            raise serializers.ValidationError("Вы уже оставили отзыв для этого тура.")

        return data

class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    tour = serializers.SerializerMethodField()
    tour_id = serializers.PrimaryKeyRelatedField(queryset=Tour.objects.all(), write_only=True, source='tour')

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'tour', 'tour_id', 'added_at']
        read_only_fields = ['id', 'user', 'added_at']

    def get_tour(self, obj):
        return {
            'id': obj.tour.id,
            'title': obj.tour.title,
            'price': obj.tour.price,
        }

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, data):
        user = self.context['request'].user
        tour = data['tour']
        if Favorite.objects.filter(user=user, tour=tour).exists():
            raise serializers.ValidationError("Этот тур уже добавлен в избранное.")
        return data