from django.contrib import admin
from .models import CarOrder

@admin.register(CarOrder)
class CarOrderAdmin(admin.ModelAdmin):
    list_display = ('car', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'car__model__name', 'car__model__brand__name')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
