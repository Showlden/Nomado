from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TourViewSet, TourCategoryViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'tours', TourViewSet)
router.register(r'categories', TourCategoryViewSet)
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
]
