# Generated by Django 5.1.7 on 2025-03-23 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autosalon', '0005_carmodel_has_climate_control_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='car',
            options={'verbose_name': 'Автомобиль', 'verbose_name_plural': 'Автомобили'},
        ),
        migrations.AddField(
            model_name='car',
            name='body_type',
            field=models.CharField(choices=[('sedan', 'Седан'), ('hatchback', 'Хэтчбек'), ('suv', 'Внедорожник'), ('crossover', 'Кроссовер'), ('wagon', 'Универсал'), ('pickup', 'Пикап'), ('minivan', 'Минивэн'), ('coupe', 'Купе'), ('convertible', 'Кабриолет')], default='sedan', max_length=20, verbose_name='Тип кузова'),
        ),
        migrations.AddField(
            model_name='car',
            name='engine_volume',
            field=models.DecimalField(decimal_places=1, default=1.6, max_digits=3, verbose_name='Объем двигателя (л)'),
        ),
        migrations.AddField(
            model_name='car',
            name='equipment_display',
            field=models.CharField(choices=[('standard', 'Стандарт'), ('comfort', 'Комфорт'), ('luxury', 'Люкс'), ('premium', 'Премиум'), ('sport', 'Спорт')], default='standard', max_length=20, verbose_name='Отображаемая комплектация'),
        ),
        migrations.AddField(
            model_name='car',
            name='fuel_type',
            field=models.CharField(choices=[('petrol', 'Бензин'), ('diesel', 'Дизель'), ('gas', 'Газ'), ('electric', 'Электро'), ('hybrid', 'Гибрид')], default='petrol', max_length=20, verbose_name='Тип топлива'),
        ),
        migrations.AddField(
            model_name='car',
            name='is_new',
            field=models.BooleanField(default=False, verbose_name='Новинка'),
        ),
        migrations.AddField(
            model_name='car',
            name='power',
            field=models.PositiveIntegerField(default=100, verbose_name='Мощность (л.с.)'),
        ),
        migrations.AddField(
            model_name='car',
            name='transmission',
            field=models.CharField(choices=[('manual', 'Механическая'), ('automatic', 'Автоматическая'), ('robot', 'Робот'), ('variator', 'Вариатор')], default='manual', max_length=20, verbose_name='Коробка передач'),
        ),
    ]
