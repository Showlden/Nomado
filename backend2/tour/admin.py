from django.contrib import admin
from .models import Tour, TourCategory, Booking

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'category', 'price', 'is_active')
    list_filter = ('category', 'is_active', 'country')
    search_fields = ('title', 'city', 'country')
    ordering = ('-created_at',)
    
@admin.register(TourCategory)
class TourCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'people_count', 'status', 'created_at')
    list_filter = ('status', 'created_at')
