from django.contrib import admin
from .models import ServiceRequest

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'car_model', 'service_type', 'service_date', 'status', 'created_at')
    list_filter = ('status', 'service_type', 'service_date')
    search_fields = ('name', 'phone', 'car_model')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
