from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class TourCategory(models.Model):
    """Категория тура"""
    name = models.CharField('Название', max_length=100, unique=True)
    
    class Meta:
        verbose_name = 'Категория тура'
        verbose_name_plural = 'Категории туров'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Tour(models.Model):
    """Модель тура"""
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    category = models.ForeignKey(
        TourCategory, 
        on_delete=models.CASCADE, 
        related_name='tours',
        verbose_name='Категория'
    )
    city = models.CharField('Город', max_length=100)
    country = models.CharField('Страна', max_length=100)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    duration_hours = models.PositiveIntegerField('Продолжительность (часы)', default=2)
    start_date = models.DateField('Дата начала')
    end_date = models.DateField('Дата окончания')
    max_people = models.PositiveIntegerField('Максимум людей', default=10)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class Booking(models.Model):
    """Модель бронирования"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('confirmed', 'Подтвержден'),
        ('cancelled', 'Отменен'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='bookings',
        verbose_name='Пользователь'
    )
    tour = models.ForeignKey(
        Tour, 
        on_delete=models.CASCADE, 
        related_name='bookings',
        verbose_name='Тур'
    )
    people_count = models.PositiveIntegerField(
        'Количество людей',
        validators=[MinValueValidator(1)],
        default=1
    )
    total_price = models.DecimalField(
        'Общая стоимость', 
        max_digits=10, 
        decimal_places=2,
        default=0.00
    )
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        """Автоматический расчет общей стоимости при сохранении"""
        if self.tour and self.people_count:
            self.total_price = self.tour.price * self.people_count
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.user.get_full_name()} - {self.tour.title}'
