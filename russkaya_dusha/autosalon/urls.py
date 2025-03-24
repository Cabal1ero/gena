from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView
app_name = 'autosalon'  # Добавляем пространство имен для приложения

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('service-center/', views.service_center, name='service_center'),
    path('models/<slug:slug>/', views.car_detail, name='car_detail'),
    path('contact-modal/', views.contact_modal, name='contact_modal'),
    path('cars/<int:car_id>/order/', views.order_car, name='order_car'),  # Новый маршрут
    path('auth/', views.auth, name='auth'),  # Используем имя функции auth вместо auth_view
    path('profile/', views.profile_dashboard, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),  # Добавляем маршрут для выхода
    path('orders/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('service-requests/<int:service_id>/cancel/', views.cancel_service, name='cancel_service'),
    
    path('accounts/', include('django.contrib.auth.urls')),  # Для сброса пароля и других стандартных функций
]
