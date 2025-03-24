from django.contrib import admin
from .models import (
    CarBrand, CarModel, Car, ModelImage, 
    Equipment, EquipmentFeature, UserProfile,
    ServiceRequest,CarOrder
)
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _

class AutosalonAdminSite(AdminSite):
    site_title = _('Русская душа')
    site_header = _('Администрирование автосалона "Русская душа"')
    index_title = _('Панель управления')

autosalon_admin_site = AutosalonAdminSite(name='autosalon_admin')

# Инлайн-модели для вложенного редактирования
class ModelImageInline(admin.TabularInline):
    model = ModelImage
    extra = 1

class EquipmentFeatureInline(admin.TabularInline):
    model = EquipmentFeature
    extra = 1

class EquipmentInline(admin.TabularInline):
    model = Equipment
    extra = 1

# Админ-модели
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Убрали country из list_display
    search_fields = ('name',)  # Убрали country из search_fields
    prepopulated_fields = {'slug': ('name',)}

class CarModelAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'brand', 'body_type', 'base_price')
    list_filter = ('brand', 'body_type')
    search_fields = ('name', 'brand__name')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ModelImageInline, EquipmentInline]

class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_model', 'equipment_type', 'price')
    list_filter = ('equipment_type', 'car_model__brand')
    search_fields = ('name', 'car_model__name', 'car_model__brand__name')
    inlines = [EquipmentFeatureInline]

class CarAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'model', 'year', 'color', 'price', 'is_available')
    list_filter = ('model__brand', 'year', 'is_available')
    search_fields = ('model__name', 'model__brand__name', 'color')
    list_per_page = 20

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    search_fields = ('user__username', 'user__email', 'phone')



class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'car_model', 'service_date', 'service_type', 'status', 'created_at')
    list_filter = ('service_type', 'status', 'service_date', 'created_at')
    search_fields = ('name', 'phone', 'car_model', 'comments')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('name', 'phone', 'user')
        }),
        ('Информация о сервисе', {
            'fields': ('car_model', 'service_date', 'service_type', 'comments')
        }),
        ('Статус', {
            'fields': ('status', 'created_at')
        }),
    )

# Регистрируем модель в нашей кастомной админке
autosalon_admin_site.register(ServiceRequest, ServiceRequestAdmin)

from .models import  ContactMessage
from django.utils import timezone

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject_display', 'created_at_formatted', 'is_processed', 'processed_by')
    list_filter = ('subject', 'is_processed', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message', 'notes')
    readonly_fields = ('created_at', 'processed_at', 'processed_by')
    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Сообщение', {
            'fields': ('subject', 'message', 'created_at')
        }),
        ('Обработка', {
            'fields': ('is_processed', 'processed_at', 'processed_by', 'notes'),
            'classes': ('collapse',),
        }),
    )
    date_hierarchy = 'created_at'
    list_per_page = 20
    
    def subject_display(self, obj):
        """Отображение темы обращения"""
        return obj.get_subject_display()
    subject_display.short_description = "Тема обращения"
    
    def created_at_formatted(self, obj):
        """Форматированная дата создания"""
        return obj.created_at.strftime('%d.%m.%Y %H:%M')
    created_at_formatted.short_description = "Дата создания"
    
    # Добавляем действия для обработки сообщений
    actions = ['mark_as_processed', 'mark_as_unprocessed']
    
    def mark_as_processed(self, request, queryset):
        """Отметить выбранные сообщения как обработанные"""
        for message in queryset:
            message.mark_as_processed(request.user)
        self.message_user(request, f"Отмечено как обработанные: {queryset.count()} сообщений")
    mark_as_processed.short_description = "Отметить как обработанные"
    
    def mark_as_unprocessed(self, request, queryset):
        """Отметить выбранные сообщения как необработанные"""
        queryset.update(is_processed=False, processed_at=None, processed_by=None)
        self.message_user(request, f"Отмечено как необработанные: {queryset.count()} сообщений")
    mark_as_unprocessed.short_description = "Отметить как необработанные"
    
    def save_model(self, request, obj, form, change):
        """При сохранении модели через админку"""
        # Если сообщение отмечено как обработанное, но дата обработки не установлена
        if obj.is_processed and not obj.processed_at:
            obj.processed_at = timezone.now()
            obj.processed_by = request.user
        super().save_model(request, obj, form, change)

class CarOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'car', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('car__model__name', 'user__username', 'user__email', 'user__first_name', 'user__last_name')
    date_hierarchy = 'created_at'
    raw_id_fields = ('car', 'user')
    
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('car', 'user', 'status')
        }),
        ('Дополнительная информация', {
            'fields': ('comment',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Если объект уже существует
            return ('car', 'user', 'created_at')
        return ('created_at',)

# Регистрируем модель в нашей кастомной админке
autosalon_admin_site.register(CarOrder, CarOrderAdmin)
# Регистрируем модель в нашей кастомной админке
autosalon_admin_site.register(ContactMessage, ContactMessageAdmin)

# Регистрация моделей в админке
autosalon_admin_site.register(CarBrand, CarBrandAdmin)
autosalon_admin_site.register(CarModel, CarModelAdmin)
autosalon_admin_site.register(Equipment, EquipmentAdmin)
autosalon_admin_site.register(Car, CarAdmin)
autosalon_admin_site.register(UserProfile, UserProfileAdmin)

# Также регистрируем модели в стандартной админке Django
admin.site.register(CarBrand, CarBrandAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ModelImage)
admin.site.register(EquipmentFeature)
