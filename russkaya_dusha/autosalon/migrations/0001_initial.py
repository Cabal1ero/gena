# Generated by Django 5.1.7 on 2025-03-22 15:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Марка автомобиля')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Марка автомобиля',
                'verbose_name_plural': 'Марки автомобилей',
            },
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Модель')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='models', to='autosalon.carbrand', verbose_name='Марка')),
            ],
            options={
                'verbose_name': 'Модель автомобиля',
                'verbose_name_plural': 'Модели автомобилей',
            },
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField(verbose_name='Год выпуска')),
                ('color', models.CharField(max_length=50, verbose_name='Цвет')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Цена')),
                ('mileage', models.PositiveIntegerField(verbose_name='Пробег (км)')),
                ('transmission', models.CharField(choices=[('manual', 'Механическая'), ('automatic', 'Автоматическая'), ('robot', 'Робот'), ('variator', 'Вариатор')], max_length=20, verbose_name='Коробка передач')),
                ('fuel_type', models.CharField(choices=[('petrol', 'Бензин'), ('diesel', 'Дизель'), ('gas', 'Газ'), ('electric', 'Электро'), ('hybrid', 'Гибрид')], max_length=20, verbose_name='Тип топлива')),
                ('engine_volume', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='Объем двигателя (л)')),
                ('power', models.PositiveIntegerField(verbose_name='Мощность (л.с.)')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('is_available', models.BooleanField(default=True, verbose_name='В наличии')),
                ('image', models.ImageField(blank=True, null=True, upload_to='cars/', verbose_name='Изображение')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars', to='autosalon.carmodel', verbose_name='Модель')),
            ],
            options={
                'verbose_name': 'Автомобиль',
                'verbose_name_plural': 'Автомобили',
            },
        ),
    ]
