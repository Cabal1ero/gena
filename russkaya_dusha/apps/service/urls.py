from django.urls import path
from . import views

app_name = 'service'

urlpatterns = [
    path('', views.service_center, name='service_center'),
    path('create/', views.create_service_request, name='create_request'),
    path('requests/', views.service_request_list, name='request_list'),
    path('requests/<int:request_id>/', views.service_request_detail, name='request_detail'),
    path('requests/<int:service_id>/cancel/', views.cancel_service, name='cancel_service'),
] 