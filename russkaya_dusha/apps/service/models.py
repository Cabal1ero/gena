from django.db import models
from django.contrib.auth.models import User

class ServiceRequest(models.Model):
    SERVICE_TYPES = [
        ('maintenance', 'Техническое обслуживание'),
        ('diagnostics', 'Диагностика'),
        ('engine_repair', 'Ремонт двигателя'),
        ('transmission_repair', 'Ремонт трансмиссии'),
        ('suspension_repair', 'Ремонт подвески'),
        ('brake_repair', 'Ремонт тормозной системы'),
        ('electrical_repair', 'Ремонт электрики'),
        ('other', 'Другое'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    car_model = models.CharField(max_length=100, verbose_name="Марка и модель автомобиля")
    service_date = models.DateField(verbose_name="Предпочтительная дата")
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES, verbose_name="Тип обслуживания")
    comments = models.TextField(blank=True, null=True, verbose_name="Комментарии")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заявки")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='service_requests', verbose_name="Пользователь")
    status = models.CharField(max_length=20, default='new', choices=[
        ('new', 'Новая'),
        ('confirmed', 'Подтверждена'),
        ('completed', 'Выполнена'),
        ('cancelled', 'Отменена'),
    ], verbose_name="Статус")
    
    def __str__(self):
        return f"Заявка на сервис от {self.name} ({self.service_date})"
    
    class Meta:
        verbose_name = "Заявка на сервис"
        verbose_name_plural = "Заявки на сервис"
        ordering = ['-created_at']
