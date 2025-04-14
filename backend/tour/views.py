from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.openapi import AutoSchema

from common.permissions import IsOwnerOrReadOnly

from .models import Tour, TourCategory, Location, Booking, Review, Favorite
from .serializers import TourSerializer, TourCategorySerializer, LocationSerializer, BookingSerializer, ReviewSerializer, FavoriteSerializer

class TourCategoryViewSet(viewsets.ModelViewSet):
    queryset = TourCategory.objects.all()
    serializer_class = TourCategorySerializer
    permission_classes = [permissions.IsAdminUser, ]
    schema = AutoSchema()

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'name']
    search_fields = ['name']
    ordering_fields = ['id', 'name']

    
class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAdminUser, ]
    schema = AutoSchema()
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'country', 'city']
    search_fields = ['country', 'city']
    ordering_fields = ['id', 'country', 'city']


class TourViewSet(viewsets.ModelViewSet):
    serializer_class = TourSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    schema = AutoSchema()
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
    'id', 'category', 'location', 'guide', 'price', 'duration', 'start_datetime',
    'end_datetime', 'max_people', 'available_slots', 'is_active', 'created_at'
    ]
    search_fields = [
        'title', 'description', 'location__city', 'location__country', 'category__name', 'guide__first_name'
    ]
    ordering_fields = [
        'id', 'price', 'duration', 'start_datetime', 'end_datetime',
        'max_people', 'available_slots', 'created_at'
    ]
    
    def get_queryset(self):
        queryset = Tour.objects.filter(is_active=True)
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset

    def perform_create(self, serializer):
        serializer.save(guide=self.request.user)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated] 
    schema = AutoSchema()
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'tour', 'booking_date', 'status', 'created_at']
    search_fields = ['tour__title', 'status']
    ordering_fields = ['booking_date', 'created_at']


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Booking.objects.all()
        return Booking.objects.filter(user=user)

    def update(self, request, *args, **kwargs):
        booking = self.get_object()
        if booking.user != request.user and not request.user.is_superuser:
            return Response({"detail": "У вас нет прав для изменения этого бронирования."}, status=403)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        booking = self.get_object()
        if booking.user != request.user and not request.user.is_superuser:
            return Response({"detail": "У вас нет прав для удаления этого бронирования."}, status=403)
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        booking = self.get_object()
        if booking.status == 'confirmed':
            return Response({"detail": "Это бронирование уже подтверждено."}, status=400)
        booking.confirm_booking()
        return Response({"detail": "Бронирование подтверждено."})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.status == 'cancelled':
            return Response({"detail": "Это бронирование уже отменено."}, status=400)
        booking.cancel_booking()
        return Response({"detail": "Бронирование отменено."})   

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]
    schema = AutoSchema()
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'tour', 'rating', 'created_at']
    search_fields = ['tour__title']
    ordering_fields = ['rating', 'created_at']



    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    schema = AutoSchema()
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'tour', 'added_at']
    search_fields = ['tour__title']
    ordering_fields = ['added_at']

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)