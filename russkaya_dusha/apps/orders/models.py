from django.db import models
from django.contrib.auth.models import User
from apps.cars.models import Car

class CarOrder(models.Model):
    ORDER_STATUS = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('confirmed', 'Подтвержден'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменен'),
    ]
    
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='orders', verbose_name="Автомобиль")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='car_orders', verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='new', verbose_name="Статус")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    
    def __str__(self):
        return f"Заказ на {self.car} от {self.user.get_full_name() or self.user.username}"
    
    class Meta:
        verbose_name = "Заказ автомобиля"
        verbose_name_plural = "Заказы автомобилей"
        ordering = ['-created_at']
