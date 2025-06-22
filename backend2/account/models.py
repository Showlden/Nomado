from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager

class User(AbstractUser):
    """Кастомная модель пользователя"""
    username = None
    email = models.EmailField('Email', unique=True)
    first_name = models.CharField('Имя', max_length=30)
    last_name = models.CharField('Фамилия', max_length=30)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()
    
    def __str__(self):
        return self.email
