# Скрипт для заполнения базы данных тестовыми данными
# Запустите его через python manage.py shell

from autosalon.models import CarBrand, CarModel, Equipment, EquipmentFeature, Car
from django.core.files import File
from django.conf import settings
import os

# Создаем бренды
lada = CarBrand.objects.create(
    name="LADA",
    description="Российский автомобильный бренд, производящий доступные и надежные автомобили для российских дорог.",
    country="Россия",
    slug="lada"
)

uaz = CarBrand.objects.create(
    name="УАЗ",
    description="Ульяновский автомобильный завод - производитель внедорожников, грузовиков и микроавтобусов повышенной проходимости.",
    country="Россия",
    slug="uaz"
)

# Создаем модели автомобилей
vesta = CarModel.objects.create(
    brand=lada,
    name="Vesta",
    description="LADA Vesta - современный и комфортный автомобиль, сочетающий в себе стильный дизайн, просторный салон и отличные технические характеристики.",
    body_type="sedan",
    base_price=1200000,
    engine_volume=1.6,
    power=106,
    transmission="manual",
    fuel_type="petrol",
    fuel_consumption=7.3,
    max_speed=182,
    acceleration=11.2,
    length=4410,
    width=1764,
    height=1497,
    wheelbase=2635,
    clearance=178,
    trunk_volume=480,
    is_new=True,
    is_popular=True,
    slug="lada-vesta"
)

patriot = CarModel.objects.create(
    brand=uaz,
    name="Патриот",
    description="УАЗ Патриот - надежный внедорожник, созданный для бездорожья и суровых условий эксплуатации. Обладает высокой проходимостью и вместительным салоном.",
    body_type="suv",
    base_price=1500000,
    engine_volume=2.7,
    power=150,
    transmission="manual",
    fuel_type="petrol",
    fuel_consumption=11.5,
    max_speed=150,
    acceleration=14.0,
    length=4750,
    width=1900,
    height=1910,
    wheelbase=2760,
    clearance=210,
    trunk_volume=650,
    is_new=False,
    is_popular=True,
    slug="uaz-patriot"
)

# Создаем комплектации для Vesta
vesta_standard = Equipment.objects.create(
    car_model=vesta,
    name="Стандарт",
    equipment_type="standard",
    price=1200000,
    description="Базовая комплектация с необходимым набором опций."
)

vesta_comfort = Equipment.objects.create(
    car_model=vesta,
    name="Комфорт",
    equipment_type="comfort",
    price=1350000,
    description="Комплектация с расширенным набором опций для комфортной езды."
)

vesta_luxury = Equipment.objects.create(
    car_model=vesta,
    name="Люкс",
    equipment_type="luxury",
    price=1500000,
    description="Максимальная комплектация со всеми доступными опциями."
)

# Создаем комплектации для Патриот
patriot_standard = Equipment.objects.create(
    car_model=patriot,
    name="Стандарт",
    equipment_type="standard",
    price=1500000,
    description="Базовая комплектация с необходимым набором опций."
)

patriot_comfort = Equipment.objects.create(
    car_model=patriot,
    name="Комфорт",
    equipment_type="comfort",
    price=1700000,
    description="Комплектация с расширенным набором опций для комфортной езды."
)

patriot_premium = Equipment.objects.create(
    car_model=patriot,
    name="Премиум",
    equipment_type="premium",
    price=1900000,
    description="Максимальная комплектация со всеми доступными опциями."
)

# Добавляем функции для комплектаций
# Для Vesta Стандарт
EquipmentFeature.objects.create(equipment=vesta_standard, name="ABS", category="safety")
EquipmentFeature.objects.create(equipment=vesta_standard, name="Подушки безопасности водителя и переднего пассажира", category="safety")
EquipmentFeature.objects.create(equipment=vesta_standard, name="Кондиционер", category="comfort")
EquipmentFeature.objects.create(equipment=vesta_standard, name="Электростеклоподъемники передних дверей", category="comfort")
EquipmentFeature.objects.create(equipment=vesta_standard, name="Аудиосистема (FM, USB, Bluetooth)", category="multimedia")

# Для Vesta Комфорт (включает все из Стандарт)
EquipmentFeature.objects.create(equipment=vesta_comfort, name="Климат-контроль", category="comfort")
EquipmentFeature.objects.create(equipment=vesta_comfort, name="Подогрев передних сидений", category="comfort")
EquipmentFeature.objects.create(equipment=vesta_comfort, name="Электростеклоподъемники задних дверей", category="comfort")
EquipmentFeature.objects.create(equipment=vesta_comfort, name="Мультимедийная система с 7\" экраном", category="multimedia")
EquipmentFeature.objects.create(equipment=vesta_comfort, name="Камера заднего вида", category="safety")

# Для Vesta Люкс (включает все из Комфорт)
EquipmentFeature.objects.create(equipment=vesta_luxury, name="Боковые подушки безопасности", category="safety")
EquipmentFeature.objects.create(equipment=vesta_luxury, name="Датчики дождя и света", category="comfort")
EquipmentFeature.objects.create(equipment=vesta_luxury, name="Подогрев лобового стекла", category="comfort")
EquipmentFeature.objects.create(equipment=vesta_luxury, name="Навигационная система", category="multimedia")
EquipmentFeature.objects.create(equipment=vesta_luxury, name="Кожаная обивка салона", category="interior")

# Создаем конкретные автомобили в наличии
Car.objects.create(
    model=vesta,
    equipment=vesta_standard,
    year=2023,
    color="Белый",
    price=1250000,
    mileage=0,
    description="Новый автомобиль LADA Vesta в базовой комплектации. Цвет: белый.",
    is_available=True,
    vin="XTA21129050123456"
)

Car.objects.create(
    model=vesta,
    equipment=vesta_comfort,
    year=2023,
    color="Красный",
    price=1400000,
    mileage=0,
    description="Новый автомобиль LADA Vesta в комплектации Комфорт. Цвет: красный.",
    is_available=True,
    vin="XTA21129050123457"
)

Car.objects.create(
    model=vesta,
    equipment=vesta_luxury,
    year=2022,
    color="Черный",
    price=1450000,
    mileage=5000,
    description="LADA Vesta в максимальной комплектации. Цвет: черный. Пробег: 5000 км.",
    is_available=True,
    vin="XTA21129050123458"
)

Car.objects.create(
    model=patriot,
    equipment=patriot_standard,
    year=2023,
    color="Зеленый",
    price=1550000,
    mileage=0,
    description="Новый УАЗ Патриот в базовой комплектации. Цвет: зеленый.",
    is_available=True,
    vin="XTT31630050123456"
)

Car.objects.create(
    model=patriot,
    equipment=patriot_premium,
    year=2022,
    color="Серебристый",
    price=1850000,
    mileage=10000,
    description="УАЗ Патриот в максимальной комплектации. Цвет: серебристый. Пробег: 10000 км.",
    is_available=True,
    vin="XTT31630050123457"
)

print("База данных успешно заполнена тестовыми данными!")
