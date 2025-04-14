from rest_framework.routers import DefaultRouter
from .views import TourViewSet, TourCategoryViewSet, LocationViewSet, BookingViewSet, ReviewViewSet, FavoriteViewSet

router = DefaultRouter()
router.register(r'list', TourViewSet, basename='tours')
router.register(r'categories', TourCategoryViewSet, basename='categories')
router.register(r'locations', LocationViewSet, basename='locations')
router.register(r'bookings', BookingViewSet, basename='bookings')
router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(r'favorites', FavoriteViewSet, basename='favorites')

urlpatterns = router.urls
