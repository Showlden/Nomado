from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse
from drf_spectacular.openapi import OpenApiTypes

from .models import Tour, TourCategory, Booking
from .serializers import TourSerializer, TourCategorySerializer, BookingSerializer, BookingListSerializer

@extend_schema_view(
    list=extend_schema(
        summary="Получить список категорий туров",
        description="Возвращает список всех категорий туров",
        responses={200: TourCategorySerializer(many=True)}
    ),
    create=extend_schema(
        summary="Создать новую категорию",
        description="Создает новую категорию туров (только для администраторов)",
        responses={201: TourCategorySerializer}
    ),
    retrieve=extend_schema(
        summary="Получить категорию по ID",
        description="Возвращает детальную информацию о категории",
        responses={200: TourCategorySerializer}
    ),
    update=extend_schema(
        summary="Обновить категорию",
        description="Обновляет существующую категорию (только для администраторов)",
        responses={200: TourCategorySerializer}
    ),
    destroy=extend_schema(
        summary="Удалить категорию",
        description="Удаляет категорию (только для администраторов)",
        responses={204: None}
    )
)
class TourCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet для управления категориями туров"""
    queryset = TourCategory.objects.all()
    serializer_class = TourCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

@extend_schema_view(
    list=extend_schema(
        summary="Получить список туров",
        description="Возвращает список всех активных туров с возможностью фильтрации и поиска",
        parameters=[
            OpenApiParameter(
                name='category',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Фильтр по ID категории'
            ),
            OpenApiParameter(
                name='city',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Фильтр по городу'
            ),
            OpenApiParameter(
                name='country',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Фильтр по стране'
            ),
            OpenApiParameter(
                name='price',
                type=OpenApiTypes.NUMBER,
                location=OpenApiParameter.QUERY,
                description='Фильтр по цене'
            ),
            OpenApiParameter(
                name='search',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Поиск по названию, описанию, городу или стране'
            ),
            OpenApiParameter(
                name='ordering',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Сортировка: price, -price, created_at, -created_at, start_date, -start_date'
            ),
        ],
        responses={200: TourSerializer(many=True)}
    ),
    create=extend_schema(
        summary="Создать новый тур",
        description="Создает новый тур (требуется аутентификация)",
        responses={201: TourSerializer}
    ),
    retrieve=extend_schema(
        summary="Получить тур по ID",
        description="Возвращает детальную информацию о туре",
        responses={200: TourSerializer}
    ),
    update=extend_schema(
        summary="Обновить тур",
        description="Обновляет существующий тур (требуется аутентификация)",
        responses={200: TourSerializer}
    ),
    destroy=extend_schema(
        summary="Удалить тур",
        description="Удаляет тур (требуется аутентификация)",
        responses={204: None}
    )
)
class TourViewSet(viewsets.ModelViewSet):
    """ViewSet для управления турами"""
    queryset = Tour.objects.filter(is_active=True)
    serializer_class = TourSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'city', 'country', 'price']
    search_fields = ['title', 'description', 'city', 'country']
    ordering_fields = ['price', 'created_at', 'start_date']
    ordering = ['-created_at']

@extend_schema_view(
    list=extend_schema(
        summary="Получить мои бронирования",
        description="Возвращает список бронирований текущего пользователя (или все для администратора)",
        parameters=[
            OpenApiParameter(
                name='status',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Фильтр по статусу: pending, confirmed, cancelled'
            ),
            OpenApiParameter(
                name='tour',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Фильтр по ID тура'
            ),
        ],
        responses={200: BookingListSerializer(many=True)}
    ),
    create=extend_schema(
        summary="Создать бронирование",
        description="Создает новое бронирование тура",
        responses={
            201: BookingSerializer,
            400: OpenApiResponse(description="Ошибка валидации (недостаточно мест, неактивный тур)")
        }
    ),
    retrieve=extend_schema(
        summary="Получить бронирование по ID",
        description="Возвращает детальную информацию о бронировании",
        responses={200: BookingSerializer}
    ),
    update=extend_schema(
        summary="Обновить бронирование",
        description="Обновляет существующее бронирование",
        responses={200: BookingSerializer}
    ),
    destroy=extend_schema(
        summary="Удалить бронирование",
        description="Удаляет бронирование",
        responses={204: None}
    )
)
class BookingViewSet(viewsets.ModelViewSet):
    """ViewSet для управления бронированиями"""
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'tour']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=user)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BookingListSerializer
        return BookingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Подтвердить бронирование",
        description="Подтверждает бронирование (только для администраторов)",
        responses={
            200: OpenApiResponse(description="Бронирование подтверждено"),
            403: OpenApiResponse(description="Недостаточно прав"),
            400: OpenApiResponse(description="Бронирование уже подтверждено")
        }
    )
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        booking = self.get_object()
        if not request.user.is_staff:
            return Response(
                {"detail": "Только администратор может подтверждать бронирования"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        if booking.status == 'confirmed':
            return Response(
                {"detail": "Бронирование уже подтверждено"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        booking.status = 'confirmed'
        booking.save()
        return Response({"detail": "Бронирование подтверждено"})

    @extend_schema(
        summary="Отменить бронирование",
        description="Отменяет бронирование",
        responses={
            200: OpenApiResponse(description="Бронирование отменено"),
            400: OpenApiResponse(description="Бронирование уже отменено")
        }
    )
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.status == 'cancelled':
            return Response(
                {"detail": "Бронирование уже отменено"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        booking.status = 'cancelled'
        booking.save()
        return Response({"detail": "Бронирование отменено"})
