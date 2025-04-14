from django.contrib import admin
from .models import Tour, TourCategory, Location, Booking, Review, Favorite

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('location', 'category', 'title')
    ordering = ('start_datetime', 'end_datetime',)
    
@admin.register(TourCategory)
class TourCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('country', 'city')
    ordering = ('country', 'city',)
    
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour')
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'rating')
    ordering = ('rating', )

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'added_at')