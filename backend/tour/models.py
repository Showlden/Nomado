from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class TourCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Категория тура"
        verbose_name_plural = "Категории туров"

    def __str__(self):
        return self.name
    
class Location(models.Model):
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    image = models.ImageField(upload_to='imgs/locations/', blank=True, null=True, verbose_name="Изображение")
    
    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"
        unique_together = ('country', 'city')


class Tour(models.Model):
    category = models.ForeignKey(TourCategory, on_delete=models.CASCADE, related_name='tours')
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='tours')
    image = models.ImageField(
        upload_to='imgs/tours/', 
        blank=True, 
        null=True, 
        verbose_name="Главное изображение"
    )
    guide = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tours'
    )
    language = models.CharField(max_length=100, default="Русский")

    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField(help_text="Формат: ЧЧ:ММ:СС")

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    max_people = models.PositiveIntegerField(default=10)
    available_slots = models.PositiveIntegerField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.available_slots = self.max_people
        super().save(*args, **kwargs)
    
    def clean(self):
        if self.start_datetime >= self.end_datetime:
            raise ValidationError("Дата окончания должна быть позже даты начала")
        
    class Meta:
        verbose_name = "Тур"
        verbose_name_plural = "Туры"

    def __str__(self):
        return f"{self.title} — {self.location}"
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings", help_text="Пользователь, который забронировал тур.")
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name="bookings", help_text="Забронированный тур.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата и время бронирования.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Дата и время последнего обновления бронирования.")
    number_of_people = models.PositiveIntegerField(help_text="Количество человек, бронирующих тур.")
    booking_date = models.DateField(help_text="Дата бронирования, для которой выбран тур.")
    status_choices = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='pending', help_text="Статус бронирования.")
    
    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        return f"Бронирование {self.id} - {self.user.first_name} на тур {self.tour.title}"

    def confirm_booking(self):
        self.status = 'confirmed'
        self.save()

    def cancel_booking(self):
        self.status = 'cancelled'
        self.save()

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'tour']
        ordering = ['-created_at']
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Review by {self.user} on {self.tour}"
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tour')
        
    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"

    def __str__(self):
        return f"{self.user} -> {self.tour}"
