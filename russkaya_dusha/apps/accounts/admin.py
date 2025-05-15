from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_phone')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'account_profile__phone')
    
    def get_phone(self, obj):
        return obj.account_profile.phone
    get_phone.short_description = 'Телефон'
    get_phone.admin_order_field = 'account_profile__phone'

# Перерегистрируем модель User с нашим кастомным админом
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
