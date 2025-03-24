# Скрипт для заполнения базы данных тестовыми данными
# Запустите его через python manage.py shell

from autosalon.models import CarBrand, CarModel, Equipment, EquipmentFeature, Car
from django.core.files import File
from django.conf import settings
import os

# Проверяем существование брендов перед созданием
lada_exists = CarBrand.objects.filter(slug='lada').exists()
uaz_exists = CarBrand.objects.filter(slug='uaz').exists()

# Создаем бренды только если они не существуют
if not lada_exists:
    lada = CarBrand.objects.create(
        name="LADA",
        description="Российский автомобильный бренд, производящий доступные и надежные автомобили для российских дорог.",
        country="Россия",
        slug="lada"
    )
    print("Создан бренд LADA")
else:
    lada = CarBrand.objects.get(slug='lada')
    print("Бренд LADA уже существует")

if not uaz_exists:
    uaz = CarBrand.objects.create(
        name="УАЗ",
        description="Ульяновский автомобильный завод - производитель внедорожников, грузовиков и микроавтобусов повышенной проходимости.",
        country="Россия",
        slug="uaz"
    )
    print("Создан бренд УАЗ")
else:
    uaz = CarBrand.objects.get(slug='uaz')
    print("Бренд УАЗ уже существует")

# Проверяем существование моделей перед созданием
vesta_exists = CarModel.objects.filter(slug='lada-vesta').exists()
patriot_exists = CarModel.objects.filter(slug='uaz-patriot').exists()

# Создаем модели только если они не существуют
if not vesta_exists:
    vesta = CarModel.objects.create(
        brand=lada,
        name="Vesta",
        description="LADA Vesta - современный и комфортный автомобиль, сочетающий в себе стильный дизайн, просторный салон и отличные технические характеристики.",
        body_type="sedan",  # Добавляем тип кузова
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
        slug="lada-vesta",
        # Добавляем поля для комфорта и оборудования
        has_climate_control=True,
        multimedia_system="7\" сенсорный экран",
        seat_heating="Передние",
        has_heated_steering_wheel=True
    )
    print("Создана модель LADA Vesta")
else:
    vesta = CarModel.objects.get(slug='lada-vesta')
    print("Модель LADA Vesta уже существует")

if not patriot_exists:
    patriot = CarModel.objects.create(
        brand=uaz,
        name="Патриот",
        description="УАЗ Патриот - надежный внедорожник, созданный для бездорожья и суровых условий эксплуатации. Обладает высокой проходимостью и вместительным салоном.",
        body_type="suv",  # Добавляем тип кузова
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
        slug="uaz-patriot",
        # Добавляем поля для комфорта и оборудования
        has_climate_control=True,
        multimedia_system="8\" сенсорный экран с навигацией",
        seat_heating="Передние и задние",
        has_heated_steering_wheel=True
    )
    print("Создана модель УАЗ Патриот")
else:
    patriot = CarModel.objects.get(slug='uaz-patriot')
    print("Модель УАЗ Патриот уже существует")


# Проверяем существование комплектаций перед созданием
# Для Vesta
vesta_standard_exists = Equipment.objects.filter(car_model=vesta, name="Стандарт").exists()
vesta_comfort_exists = Equipment.objects.filter(car_model=vesta, name="Комфорт").exists()
vesta_luxury_exists = Equipment.objects.filter(car_model=vesta, name="Люкс").exists()

# Для Патриот
patriot_standard_exists = Equipment.objects.filter(car_model=patriot, name="Стандарт").exists()
patriot_comfort_exists = Equipment.objects.filter(car_model=patriot, name="Комфорт").exists()
patriot_premium_exists = Equipment.objects.filter(car_model=patriot, name="Премиум").exists()

# Создаем комплектации для Vesta
if not vesta_standard_exists:
    vesta_standard = Equipment.objects.create(
        car_model=vesta,
        name="Стандарт",
        equipment_type="standard",
        price=1200000,
        description="Базовая комплектация с необходимым набором опций."
    )
    print("Создана комплектация LADA Vesta Стандарт")
else:
    vesta_standard = Equipment.objects.get(car_model=vesta, name="Стандарт")
    print("Комплектация LADA Vesta Стандарт уже существует")

if not vesta_comfort_exists:
    vesta_comfort = Equipment.objects.create(
        car_model=vesta,
        name="Комфорт",
        equipment_type="comfort",
        price=1350000,
        description="Комплектация с расширенным набором опций для комфортной езды."
    )
    print("Создана комплектация LADA Vesta Комфорт")
else:
    vesta_comfort = Equipment.objects.get(car_model=vesta, name="Комфорт")
    print("Комплектация LADA Vesta Комфорт уже существует")

if not vesta_luxury_exists:
    vesta_luxury = Equipment.objects.create(
        car_model=vesta,
        name="Люкс",
        equipment_type="luxury",
        price=1500000,
        description="Максимальная комплектация со всеми доступными опциями."
    )
    print("Создана комплектация LADA Vesta Люкс")
else:
    vesta_luxury = Equipment.objects.get(car_model=vesta, name="Люкс")
    print("Комплектация LADA Vesta Люкс уже существует")

# Создаем комплектации для Патриот
if not patriot_standard_exists:
    patriot_standard = Equipment.objects.create(
        car_model=patriot,
        name="Стандарт",
        equipment_type="standard",
        price=1500000,
        description="Базовая комплектация с необходимым набором опций."
    )
    print("Создана комплектация УАЗ Патриот Стандарт")
else:
    patriot_standard = Equipment.objects.get(car_model=patriot, name="Стандарт")
    print("Комплектация УАЗ Патриот Стандарт уже существует")

if not patriot_comfort_exists:
    patriot_comfort = Equipment.objects.create(
        car_model=patriot,
        name="Комфорт",
        equipment_type="comfort",
        price=1700000,
        description="Комплектация с расширенным набором опций для комфортной езды."
    )
    print("Создана комплектация УАЗ Патриот Комфорт")
else:
    patriot_comfort = Equipment.objects.get(car_model=patriot, name="Комфорт")
    print("Комплектация УАЗ Патриот Комфорт уже существует")

if not patriot_premium_exists:
    patriot_premium = Equipment.objects.create(
        car_model=patriot,
        name="Премиум",
        equipment_type="premium",
        price=1900000,
        description="Максимальная комплектация со всеми доступными опциями."
    )
    print("Создана комплектация УАЗ Патриот Премиум")
else:
    patriot_premium = Equipment.objects.get(car_model=patriot, name="Премиум")
    print("Комплектация УАЗ Патриот Премиум уже существует")

# Проверяем существование функций комплектаций перед созданием
# Для Vesta Стандарт
if not EquipmentFeature.objects.filter(equipment=vesta_standard, name="ABS").exists():
    EquipmentFeature.objects.create(equipment=vesta_standard, name="ABS", category="safety")
    print("Добавлена функция ABS для LADA Vesta Стандарт")

if not EquipmentFeature.objects.filter(equipment=vesta_standard, name="Подушки безопасности водителя и переднего пассажира").exists():
    EquipmentFeature.objects.create(equipment=vesta_standard, name="Подушки безопасности водителя и переднего пассажира", category="safety")
    print("Добавлена функция Подушки безопасности для LADA Vesta Стандарт")

if not EquipmentFeature.objects.filter(equipment=vesta_standard, name="Кондиционер").exists():
    EquipmentFeature.objects.create(equipment=vesta_standard, name="Кондиционер", category="comfort")
    print("Добавлена функция Кондиционер для LADA Vesta Стандарт")

if not EquipmentFeature.objects.filter(equipment=vesta_standard, name="Электростеклоподъемники передних дверей").exists():
    EquipmentFeature.objects.create(equipment=vesta_standard, name="Электростеклоподъемники передних дверей", category="comfort")
    print("Добавлена функция Электростеклоподъемники для LADA Vesta Стандарт")

if not EquipmentFeature.objects.filter(equipment=vesta_standard, name="Аудиосистема (FM, USB, Bluetooth)").exists():
    EquipmentFeature.objects.create(equipment=vesta_standard, name="Аудиосистема (FM, USB, Bluetooth)", category="multimedia")
    print("Добавлена функция Аудиосистема для LADA Vesta Стандарт")

# Для Vesta Комфорт
if not EquipmentFeature.objects.filter(equipment=vesta_comfort, name="Климат-контроль").exists():
    EquipmentFeature.objects.create(equipment=vesta_comfort, name="Климат-контроль", category="comfort")
    print("Добавлена функция Климат-контроль для LADA Vesta Комфорт")

if not EquipmentFeature.objects.filter(equipment=vesta_comfort, name="Подогрев передних сидений").exists():
    EquipmentFeature.objects.create(equipment=vesta_comfort, name="Подогрев передних сидений", category="comfort")
    print("Добавлена функция Подогрев сидений для LADA Vesta Комфорт")

# Проверяем существование автомобилей перед созданием
vesta_white_exists = Car.objects.filter(model=vesta, color="Белый", vin="XTA21129050123456").exists()
vesta_red_exists = Car.objects.filter(model=vesta, color="Красный", vin="XTA21129050123457").exists()
vesta_black_exists = Car.objects.filter(model=vesta, color="Черный", vin="XTA21129050123458").exists()
patriot_green_exists = Car.objects.filter(model=patriot, color="Зеленый", vin="XTT31630050123456").exists()
patriot_silver_exists = Car.objects.filter(model=patriot, color="Серебристый", vin="XTT31630050123457").exists()

# Создаем конкретные автомобили в наличии
if not vesta_white_exists:
    Car.objects.create(
        model=vesta,
        equipment=vesta_standard,
        year=2023,
        color="Белый",
        price=1250000,
        mileage=0,
        transmission="manual",
        fuel_type="petrol",
        body_type="sedan",  # Добавляем тип кузова
        equipment_display="standard",  # Добавляем отображаемую комплектацию
        engine_volume=1.6,
        power=106,
        description="Новый автомобиль LADA Vesta в базовой комплектации. Цвет: белый.",
        is_available=True,
        vin="XTA21129050123456"
    )
    print("Создан автомобиль LADA Vesta белого цвета")

if not vesta_red_exists:
    Car.objects.create(
        model=vesta,
        equipment=vesta_comfort,
        year=2023,
        color="Красный",
        price=1400000,
        mileage=0,
        transmission="automatic",
        fuel_type="petrol",
        body_type="sedan",  # Добавляем тип кузова
        equipment_display="comfort",  # Добавляем отображаемую комплектацию
        engine_volume=1.6,
        power=106,
        description="Новый автомобиль LADA Vesta в комплектации Комфорт. Цвет: красный.",
        is_available=True,
        vin="XTA21129050123457"
    )
    print("Создан автомобиль LADA Vesta красного цвета")

if not vesta_black_exists:
    Car.objects.create(
        model=vesta,
        equipment=vesta_luxury,
        year=2022,
        color="Черный",
        price=1550000,
        mileage=5000,
        transmission="automatic",
        fuel_type="petrol",
        body_type="sedan",  # Добавляем тип кузова
        equipment_display="luxury",  # Добавляем отображаемую комплектацию
        engine_volume=1.6,
        power=106,
        description="Автомобиль LADA Vesta в максимальной комплектации. Цвет: черный. Небольшой пробег.",
        is_available=True,
        vin="XTA21129050123458"
    )
    print("Создан автомобиль LADA Vesta черного цвета")

if not patriot_green_exists:
    Car.objects.create(
        model=patriot,
        equipment=patriot_standard,
        year=2023,
        color="Зеленый",
        price=1550000,
        mileage=0,
        transmission="manual",
        fuel_type="petrol",
        body_type="suv",  # Добавляем тип кузова
        equipment_display="standard",  # Добавляем отображаемую комплектацию
        engine_volume=2.7,
        power=150,
        description="Новый автомобиль УАЗ Патриот в базовой комплектации. Цвет: зеленый.",
        is_available=True,
        vin="XTT31630050123456"
    )
    print("Создан автомобиль УАЗ Патриот зеленого цвета")

if not patriot_silver_exists:
    Car.objects.create(
        model=patriot,
        equipment=patriot_premium,
        year=2022,
        color="Серебристый",
        price=1950000,
        mileage=10000,
        transmission="manual",
        fuel_type="petrol",
        body_type="suv",  # Добавляем тип кузова
        equipment_display="premium",  # Добавляем отображаемую комплектацию
        engine_volume=2.7,
        power=150,
        description="Автомобиль УАЗ Патриот в максимальной комплектации. Цвет: серебристый. Небольшой пробег.",
        is_available=True,
        vin="XTT31630050123457"
    )
    print("Создан автомобиль УАЗ Патриот серебристого цвета")

# Создаем еще несколько автомобилей с разными комплектациями
vesta_blue_exists = Car.objects.filter(model=vesta, color="Синий", vin="XTA21129050123459").exists()
patriot_black_exists = Car.objects.filter(model=patriot, color="Черный", vin="XTT31630050123458").exists()

if not vesta_blue_exists:
    Car.objects.create(
        model=vesta,
        equipment=vesta_comfort,
        year=2023,
        color="Синий",
        price=1400000,
        mileage=0,
        transmission="robot",
        fuel_type="petrol",
        body_type="sedan",  # Добавляем тип кузова
        equipment_display="sport",  # Добавляем отображаемую комплектацию
        engine_volume=1.8,
        power=122,
        description="Новый автомобиль LADA Vesta в спортивной комплектации. Цвет: синий.",
        is_available=True,
        vin="XTA21129050123459"
    )
    print("Создан автомобиль LADA Vesta синего цвета")

if not patriot_black_exists:
    Car.objects.create(
        model=patriot,
        equipment=patriot_premium,
        year=2023,
        color="Черный",
        price=2000000,
        mileage=0,
        transmission="automatic",
        fuel_type="diesel",
        body_type="suv",  # Добавляем тип кузова
        equipment_display="luxury",  # Добавляем отображаемую комплектацию
        engine_volume=2.2,
        power=130,
        description="Новый автомобиль УАЗ Патриот в люксовой комплектации с дизельным двигателем. Цвет: черный.",
        is_available=True,
        vin="XTT31630050123458"
    )
    print("Создан автомобиль УАЗ Патриот черного цвета")

# Создаем автомобиль с шуточной комплектацией (как в вашем примере)
vesta_joke_exists = Car.objects.filter(model=vesta, color="Белый", vin="XTA21129050123460").exists()

if not vesta_joke_exists:
    Car.objects.create(
        model=vesta,
        equipment=vesta_standard,
        year=2030,
        color="Белый",
        price=5200000,
        mileage=0,
        transmission="manual",
        fuel_type="petrol",
        body_type="sedan",  # Добавляем тип кузова
        equipment_display="standard",  # Добавляем отображаемую комплектацию
        engine_volume=1.6,
        power=106,
        description="Футуристический автомобиль LADA Vesta 2030 года. Отсутствует. Брычка. На честном слове.",
        is_available=True,
        is_new=True,  # Отмечаем как новинку
        vin="XTA21129050123460"
    )
    print("Создан шуточный автомобиль LADA Vesta 2030 года")

print("База данных успешно заполнена тестовыми данными!")
