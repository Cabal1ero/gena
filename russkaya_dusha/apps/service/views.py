from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ServiceRequest
from django.utils import timezone

def service_center(request):
    """Представление для страницы сервисного центра"""
    return render(request, 'service/service_center.html')

@login_required
def create_service_request(request):
    """Создание новой заявки на сервис"""
    if request.method == 'POST':
        # Здесь будет логика создания заявки
        pass
    return render(request, 'service/create_request.html')

@login_required
def service_request_list(request):
    """Список заявок пользователя"""
    user_requests = ServiceRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'service/request_list.html', {'requests': user_requests})

@login_required
def service_request_detail(request, request_id):
    """Детальная информация о заявке"""
    service_request = get_object_or_404(ServiceRequest, id=request_id, user=request.user)
    return render(request, 'service/request_detail.html', {'request': service_request})

@login_required
def cancel_service(request, service_id):
    """Отмена заявки на сервис"""
    service_request = get_object_or_404(ServiceRequest, id=service_id, user=request.user)
    
    if service_request.status == 'new':
        service_request.status = 'cancelled'
        service_request.save()
        messages.success(request, 'Заявка успешно отменена')
    else:
        messages.error(request, 'Невозможно отменить заявку в текущем статусе')
    
    return redirect('service:request_list')
