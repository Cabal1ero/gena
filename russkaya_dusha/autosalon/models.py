from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.urls import reverse


class CarBrand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Марка автомобиля")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    image = models.ImageField(upload_to='brands/', blank=True, null=True, verbose_name="Логотип")
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name="Страна производитель")
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name="URL-идентификатор")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Марка автомобиля"
        verbose_name_plural = "Марки автомобилей"
        ordering = ['name']

class CarModel(models.Model):
    BODY_TYPE_CHOICES = [
        ('sedan', 'Седан'),
        ('hatchback', 'Хэтчбек'),
        ('suv', 'Внедорожник'),
        ('crossover', 'Кроссовер'),
        ('wagon', 'Универсал'),
        ('pickup', 'Пикап'),
        ('minivan', 'Минивэн'),
        ('coupe', 'Купе'),
        ('convertible', 'Кабриолет'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('manual', 'Механическая'),
        ('automatic', 'Автоматическая'),
        ('robot', 'Робот'),
        ('variator', 'Вариатор'),
    ]
    
    FUEL_CHOICES = [
        ('petrol', 'Бензин'),
        ('diesel', 'Дизель'),
        ('gas', 'Газ'),
        ('electric', 'Электро'),
        ('hybrid', 'Гибрид'),
    ]
    
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, related_name='models', verbose_name="Марка")
    name = models.CharField(max_length=100, verbose_name="Модель")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    body_type = models.CharField(max_length=20, choices=BODY_TYPE_CHOICES, default='sedan', verbose_name="Тип кузова")
    base_price = models.DecimalField(max_digits=12, decimal_places=2, default=1000000, verbose_name="Базовая цена")
    image = models.ImageField(upload_to='models/', blank=True, null=True, verbose_name="Основное изображение")
    engine_volume = models.DecimalField(max_digits=3, decimal_places=1, default=1.6, verbose_name="Объем двигателя (л)")
    power = models.PositiveIntegerField(default=100, verbose_name="Мощность (л.с.)")
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='manual', verbose_name="Коробка передач")
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default='petrol', verbose_name="Тип топлива")
    fuel_consumption = models.DecimalField(max_digits=3, decimal_places=1, default=7.5, blank=True, null=True, verbose_name="Расход топлива (л/100км)")
    max_speed = models.PositiveIntegerField(default=180, blank=True, null=True, verbose_name="Максимальная скорость (км/ч)")
    acceleration = models.DecimalField(max_digits=3, decimal_places=1, default=10.0, blank=True, null=True, verbose_name="Разгон до 100 км/ч (сек)")
    length = models.PositiveIntegerField(default=4500, blank=True, null=True, verbose_name="Длина (мм)")
    width = models.PositiveIntegerField(default=1800, blank=True, null=True, verbose_name="Ширина (мм)")
    height = models.PositiveIntegerField(default=1500, blank=True, null=True, verbose_name="Высота (мм)")
    wheelbase = models.PositiveIntegerField(default=2600, blank=True, null=True, verbose_name="Колесная база (мм)")
    clearance = models.PositiveIntegerField(default=160, blank=True, null=True, verbose_name="Дорожный просвет (мм)")
    trunk_volume = models.PositiveIntegerField(default=400, blank=True, null=True, verbose_name="Объем багажника (л)")
    is_new = models.BooleanField(default=False, verbose_name="Новинка")
    is_popular = models.BooleanField(default=False, verbose_name="Популярная модель")
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name="URL-идентификатор")
    has_climate_control = models.BooleanField(default=True, verbose_name="Климат-контроль")
    multimedia_system = models.CharField(max_length=100, blank=True, null=True, verbose_name="Мультимедийная система")
    seat_heating = models.CharField(max_length=100, blank=True, null=True, verbose_name="Подогрев сидений")
    has_heated_steering_wheel = models.BooleanField(default=True, verbose_name="Подогрев руля")
    trunk_volume = models.PositiveIntegerField(blank=True, null=True, verbose_name="Объем багажника (л)")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.brand.name}-{self.name}")
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('autosalon:car_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return f"{self.brand.name} {self.name}"
    
    class Meta:
        verbose_name = "Модель автомобиля"
        verbose_name_plural = "Модели автомобилей"
        ordering = ['brand__name', 'name']

class ModelImage(models.Model):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='images', verbose_name="Модель автомобиля")
    image = models.ImageField(upload_to='model_images/', verbose_name="Изображение")
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name="Заголовок")
    is_main = models.BooleanField(default=False, verbose_name="Основное изображение")
    
    def __str__(self):
        return f"Изображение {self.car_model}"
    
    class Meta:
        verbose_name = "Изображение модели"
        verbose_name_plural = "Изображения моделей"

class Equipment(models.Model):
    EQUIPMENT_TYPE_CHOICES = [
        ('standard', 'Стандарт'),
        ('comfort', 'Комфорт'),
        ('luxury', 'Люкс'),
        ('premium', 'Премиум'),
        ('sport', 'Спорт'),
    ]
    
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='equipments', verbose_name="Модель автомобиля")
    name = models.CharField(max_length=100, verbose_name="Название комплектации")
    equipment_type = models.CharField(max_length=20, choices=EQUIPMENT_TYPE_CHOICES, verbose_name="Тип комплектации")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Цена")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    
    def __str__(self):
        return f"{self.car_model} - {self.name}"
    
    class Meta:
        verbose_name = "Комплектация"
        verbose_name_plural = "Комплектации"
        ordering = ['price']

class EquipmentFeature(models.Model):
    FEATURE_CATEGORY_CHOICES = [
        ('safety', 'Безопасность'),
        ('comfort', 'Комфорт'),
        ('multimedia', 'Мультимедиа'),
        ('exterior', 'Экстерьер'),
        ('interior', 'Интерьер'),
        ('other', 'Другое'),
    ]
    
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='features', verbose_name="Комплектация")
    name = models.CharField(max_length=255, verbose_name="Название функции")
    category = models.CharField(max_length=20, choices=FEATURE_CATEGORY_CHOICES, verbose_name="Категория")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Функция комплектации"
        verbose_name_plural = "Функции комплектаций"

class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('manual', 'Механическая'),
        ('automatic', 'Автоматическая'),
        ('robot', 'Робот'),
        ('variator', 'Вариатор'),
    ]
    
    FUEL_CHOICES = [
        ('petrol', 'Бензин'),
        ('diesel', 'Дизель'),
        ('gas', 'Газ'),
        ('electric', 'Электро'),
        ('hybrid', 'Гибрид'),
    ]
    
    # Добавляем choices для типа кузова
    BODY_TYPE_CHOICES = [
        ('sedan', 'Седан'),
        ('hatchback', 'Хэтчбек'),
        ('suv', 'Внедорожник'),
        ('crossover', 'Кроссовер'),
        ('wagon', 'Универсал'),
        ('pickup', 'Пикап'),
        ('minivan', 'Минивэн'),
        ('coupe', 'Купе'),
        ('convertible', 'Кабриолет'),
    ]
    
    # Добавляем choices для комплектации
    EQUIPMENT_CHOICES = [
        ('standard', 'Стандарт'),
        ('comfort', 'Комфорт'),
        ('luxury', 'Люкс'),
        ('premium', 'Премиум'),
        ('sport', 'Спорт'),
    ]
    
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='cars', verbose_name="Модель")
    equipment = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True, blank=True, related_name='cars', verbose_name="Комплектация")
    year = models.PositiveIntegerField(verbose_name="Год выпуска")
    color = models.CharField(max_length=50, verbose_name="Цвет")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Цена")
    mileage = models.PositiveIntegerField(verbose_name="Пробег (км)")
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='manual', verbose_name="Коробка передач")

    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default='petrol', verbose_name="Тип топлива")  # Добавляем default
    
    # Добавляем поле для типа кузова с default значением
    body_type = models.CharField(max_length=20, choices=BODY_TYPE_CHOICES, default='sedan', verbose_name="Тип кузова")
    
    # Добавляем поле для отображения комплектации с default значением
    equipment_display = models.CharField(max_length=20, choices=EQUIPMENT_CHOICES, default='standard', verbose_name="Отображаемая комплектация")
    
    engine_volume = models.DecimalField(max_digits=3, decimal_places=1, default=1.6, verbose_name="Объем двигателя (л)")  # Добавляем default
    power = models.PositiveIntegerField(default=100, verbose_name="Мощность (л.с.)")  # Добавляем default
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    is_available = models.BooleanField(default=True, verbose_name="В наличии")
    image = models.ImageField(upload_to='cars/', blank=True, null=True, verbose_name="Изображение")
    
    # Добавляем поле VIN с возможностью null
    vin = models.CharField(max_length=17, blank=True, null=True, verbose_name="VIN-номер")
    
    # Добавляем поле для отметки новинки
    is_new = models.BooleanField(default=False, verbose_name="Новинка")
    
    def __str__(self):
        return f"{self.model} ({self.year})"
    
    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"

from django.db import models
from django.utils import timezone

class ContactMessage(models.Model):
    SUBJECT_CHOICES = [
        ('general', 'Общий вопрос'),
        ('sales', 'Покупка автомобиля'),
        ('service', 'Сервисное обслуживание'),
        ('test_drive', 'Запись на тест-драйв'),
        ('feedback', 'Отзыв о работе автосалона'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default='general', verbose_name="Тема обращения")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_processed = models.BooleanField(default=False, verbose_name="Обработано")
    processed_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата обработки")
    processed_by = models.ForeignKey(
        'auth.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='processed_messages',
        verbose_name="Кто обработал"
    )
    notes = models.TextField(blank=True, null=True, verbose_name="Примечания")
    
    def mark_as_processed(self, user=None):
        """Отметить сообщение как обработанное"""
        self.is_processed = True
        self.processed_at = timezone.now()
        self.processed_by = user
        self.save()
    
    def __str__(self):
        return f"{self.name} - {self.get_subject_display()} ({self.created_at.strftime('%d.%m.%Y %H:%M')})"
    
    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ['-created_at']

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
