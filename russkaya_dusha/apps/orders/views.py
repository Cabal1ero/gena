from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CarOrder
from apps.cars.models import Car

# Create your views here.

@login_required
def order_car(request, car_id):
    """Создание заказа на автомобиль"""
    car = get_object_or_404(Car, id=car_id)
    
    if request.method == 'POST':
        comment = request.POST.get('comment', '')
        
        # Проверяем, нет ли уже активного заказа на этот автомобиль
        if CarOrder.objects.filter(car=car, status__in=['new', 'processing', 'confirmed']).exists():
            messages.error(request, 'Этот автомобиль уже заказан')
            return redirect('cars:car_detail', slug=car.model.slug)
        
        # Создаем новый заказ
        order = CarOrder.objects.create(
            car=car,
            user=request.user,
            comment=comment
        )
        
        messages.success(request, 'Заказ успешно создан')
        return redirect('orders:order_detail', order_id=order.id)
    
    return render(request, 'orders/create_order.html', {'car': car})

@login_required
def order_list(request):
    """Список заказов пользователя"""
    orders = CarOrder.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    """Детальная информация о заказе"""
    order = get_object_or_404(CarOrder, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def cancel_order(request, order_id):
    """Отмена заказа"""
    order = get_object_or_404(CarOrder, id=order_id, user=request.user)
    
    if order.status in ['new', 'processing']:
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'Заказ успешно отменен')
    else:
        messages.error(request, 'Невозможно отменить заказ в текущем статусе')
    
    return redirect('orders:order_list')
