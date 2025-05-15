from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import Car, CarBrand, CarModel, Equipment, CarOrder, ServiceRequest
from apps.accounts.models import UserProfile

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import get_object_or_404



def home(request):
    # Получаем все модели автомобилей
    car_models = CarModel.objects.all()
    
    # Получаем все бренды
    brands = CarBrand.objects.all()
    
    return render(request, 'home.html', {
        'car_models': car_models,
        'brands': brands,
    })

def car_detail(request, slug):
    # Получаем модель автомобиля по slug или возвращаем 404, если не найдена
    car_model = get_object_or_404(CarModel, slug=slug)
    
    # Получаем все комплектации для данной модели
    equipments = Equipment.objects.filter(car_model=car_model)
    
    # Получаем похожие модели (например, того же бренда)
    similar_models = CarModel.objects.filter(brand=car_model.brand).exclude(id=car_model.id)[:3]
    
    # Получаем автомобили в наличии для данной модели
    available_cars = Car.objects.filter(model=car_model, is_available=True)
    
    return render(request, 'car_detail.html', {
        'car_model': car_model,
        'equipments': equipments,
        'similar_models': similar_models,
        'available_cars': available_cars,
    })
def about(request):
    return render(request, 'about.html')

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Car, CarBrand, CarModel
from django.db.models import Min, Max

def services(request):
    # Получаем все автомобили
    cars_list = Car.objects.all()
    
    # Получаем уникальные годы для фильтра
    years = Car.objects.values_list('year', flat=True).distinct().order_by('-year')
    
    # Применяем фильтры из GET-параметров
    # Фильтр по году
    year_from = request.GET.get('year_from')
    year_to = request.GET.get('year_to')
    
    if year_from:
        cars_list = cars_list.filter(year__gte=year_from)
    if year_to:
        cars_list = cars_list.filter(year__lte=year_to)
    
    # Фильтр по комплектации
    equipment = request.GET.get('equipment')
    if equipment:
        cars_list = cars_list.filter(equipment_display=equipment)
    
    # Фильтр по типу кузова (может быть несколько значений)
    body_types = request.GET.getlist('body_type')
    if body_types:
        cars_list = cars_list.filter(body_type__in=body_types)
    
    # Фильтр по цвету (может быть несколько значений)
    colors = request.GET.getlist('color')
    if colors:
        # Преобразуем значения из формы в соответствующие значения в базе данных
        color_mapping = {
            'white': 'Белый',
            'black': 'Черный',
            'silver': 'Серебристый',
            'gray': 'Серый',
            'red': 'Красный',
            'blue': 'Синий',
            'green': 'Зеленый',
            'brown': 'Коричневый'
        }
        db_colors = [color_mapping.get(color, color) for color in colors if color in color_mapping]
        cars_list = cars_list.filter(color__in=db_colors)
    
    # Фильтр по типу топлива (может быть несколько значений)
    fuel_types = request.GET.getlist('fuel_type')
    if fuel_types:
        cars_list = cars_list.filter(fuel_type__in=fuel_types)
    
    # Фильтр по коробке передач (может быть несколько значений)
    transmissions = request.GET.getlist('transmission')
    if transmissions:
        cars_list = cars_list.filter(transmission__in=transmissions)
    
    # Фильтр по цене
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    
    if price_from:
        cars_list = cars_list.filter(price__gte=price_from)
    if price_to:
        cars_list = cars_list.filter(price__lte=price_to)
    
    # Фильтр по наличию
    is_available = request.GET.get('is_available')
    if is_available == 'true':
        cars_list = cars_list.filter(is_available=True)
    
    # Фильтр по новинкам
    is_new = request.GET.get('is_new')
    if is_new == 'true':
        cars_list = cars_list.filter(is_new=True)
    
    # Пагинация результатов
    paginator = Paginator(cars_list, 9)  # 9 автомобилей на страницу
    page = request.GET.get('page')
    
    try:
        cars = paginator.page(page)
    except PageNotAnInteger:
        # Если page не является целым числом, показываем первую страницу
        cars = paginator.page(1)
    except EmptyPage:
        # Если page больше максимального числа страниц, показываем последнюю
        cars = paginator.page(paginator.num_pages)
    
    # Получаем минимальную и максимальную цены для подсказок в фильтре цены
    price_range = Car.objects.aggregate(min_price=Min('price'), max_price=Max('price'))
    
    context = {
        'cars': cars,
        'years': years,
        'price_range': price_range,
        # Добавляем списки для выпадающих списков и чекбоксов
        'body_types': Car.BODY_TYPE_CHOICES,
        'equipment_types': Car.EQUIPMENT_CHOICES,
        'fuel_types': Car.FUEL_CHOICES,
        'transmission_types': Car.TRANSMISSION_CHOICES,
    }
    
    return render(request, 'services.html', context)

def service_center(request):
    return render(request, 'service_center.html')


from django.http import JsonResponse
from .forms import ContactForm 
def contact_modal(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'message': 'Ваше сообщение успешно отправлено!'
            })
        else:
            # Возвращаем ошибки валидации
            errors = {field: error[0] for field, error in form.errors.items()}
            return JsonResponse({
                'success': False,
                'errors': errors
            })
    
    # Если запрос не AJAX или не POST, возвращаем ошибку
    return JsonResponse({'success': False, 'message': 'Неверный запрос'}, status=400)


from django.contrib.auth.decorators import login_required


@login_required
def profile_dashboard(request):
    """Отображение личного кабинета пользователя"""
    # Получаем избранные автомобили пользователя (предполагается, что есть модель Favorite)
    service_requests = ServiceRequest.objects.filter(user=request.user)
    orders = CarOrder.objects.filter(user=request.user)
    # В реальном приложении здесь будет что-то вроде:
    # favorite_cars = Favorite.objects.filter(user=request.user).select_related('car')
    
    context = {
        'service_requests': service_requests,
        'orders': orders,
    }
    
    return render(request, 'profile/dashboard.html', context)

@login_required
def profile_update(request):
    """Обновление профиля пользователя и изменение пароля"""
    if request.method == 'POST':
        action = request.POST.get('action', 'update_profile')
        
        # Обработка обновления профиля
        if action == 'update_profile':
            # Обновляем данные пользователя
            user = request.user
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')
            user.save()
            
            # Обновляем профиль пользователя
            profile = user.profile
            profile.phone = request.POST.get('phone', '')
            
            # Обработка аватара
            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
            
            # Проверяем флаг удаления аватара
            if request.POST.get('remove_avatar') == 'true':
                profile.avatar = None
                
            profile.save()
            
            messages.success(request, 'Профиль успешно обновлен!')
        
        # Обработка изменения пароля
        elif action == 'change_password':
            old_password = request.POST.get('old_password', '')
            new_password1 = request.POST.get('new_password1', '')
            new_password2 = request.POST.get('new_password2', '')
            
            # Проверка корректности старого пароля
            if not request.user.check_password(old_password):
                messages.error(request, 'Неверный текущий пароль.')
                return redirect('autosalon:profile')
            
            # Проверка совпадения новых паролей
            if new_password1 != new_password2:
                messages.error(request, 'Новые пароли не совпадают.')
                return redirect('autosalon:profile')
            
            # Проверка сложности пароля (можно добавить дополнительные проверки)
            if len(new_password1) < 4:
                messages.error(request, 'Пароль должен содержать не менее 4 символов.')
                return redirect('autosalon:profile')
            
            # Изменение пароля
            request.user.set_password(new_password1)
            request.user.save()
            
            # Обновляем сессию, чтобы пользователь не вышел из системы
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, request.user)
            
            messages.success(request, 'Пароль успешно изменен!')
        
        # Возвращаемся на страницу профиля
        return redirect('autosalon:profile')
    
    # Если запрос не POST, просто перенаправляем на страницу профиля
    return redirect('autosalon:profile')

from .forms import ServiceRequestForm

def service_center(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            
            # Если пользователь авторизован, привязываем заявку к нему
            if request.user.is_authenticated:
                service_request.user = request.user
                
            service_request.save()
            messages.success(request, 'Ваша заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.')
            return redirect('autosalon:service_center')
    else:
        # Предзаполняем форму данными пользователя, если он авторизован
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'name': f"{request.user.first_name} {request.user.last_name}".strip(),
                'phone': request.user.profile.phone if hasattr(request.user, 'profile') else '',
            }
        form = ServiceRequestForm(initial=initial_data)
    
    return render(request, 'service_center.html', {'form': form})

@login_required
def order_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    # Проверяем, доступен ли автомобиль
    if not car.is_available:
        messages.error(request, "К сожалению, этот автомобиль уже недоступен для заказа.")
        return redirect('autosalon:car_detail', car_id=car_id)
    
    # Создаем заказ
    order = CarOrder.objects.create(
        car=car,
        user=request.user,
        status='new'
    )
    
    # Отправляем уведомление администратору (можно реализовать позже)
    
    messages.success(request, f"Ваш заказ на {car.model} успешно создан! Наш менеджер свяжется с вами в ближайшее время.")
    
    # Перенаправляем на страницу с деталями автомобиля
    return redirect('autosalon:profile')

@login_required
def cancel_order(request, order_id):
    """Отмена заказа пользователем"""
    # Получаем заказ или возвращаем 404, если заказ не найден
    order = get_object_or_404(CarOrder, id=order_id)
    
    # Проверяем, принадлежит ли заказ текущему пользователю
    if order.user != request.user:
        messages.error(request, 'У вас нет прав для отмены этого заказа.')
        return redirect('autosalon:profile')
    
    # Проверяем, можно ли отменить заказ (только статусы 'new' и 'processing')
    if order.status not in ['new', 'processing']:
        messages.error(request, 'Этот заказ нельзя отменить, так как он уже обрабатывается или выполнен.')
        return redirect('autosalon:profile')
    
    # Если метод POST, отменяем заказ
    if request.method == 'POST':
        # Меняем статус заказа на 'cancelled'
        order.status = 'cancelled'
        order.save()
        
        messages.success(request, f'Заказ №{order.id} успешно отменен.')
        
        # Здесь можно добавить дополнительную логику, например:
        # - отправка уведомления администратору
        # - возврат средств, если была предоплата
        # - освобождение зарезервированных товаров и т.д.
        
    # Перенаправляем на страницу профиля с активной вкладкой "Заказы"
    return redirect('autosalon:profile')

@login_required
def cancel_service(request, service_id):
    """Отмена заявки на сервисное обслуживание"""
    # Получаем заявку или возвращаем 404, если заявка не найдена
    service_request = get_object_or_404(ServiceRequest, id=service_id)
    
    # Проверяем, принадлежит ли заявка текущему пользователю
    if service_request.user != request.user:
        messages.error(request, 'У вас нет прав для отмены этой заявки.')
        return redirect('autosalon:profile')
    
    # Проверяем, можно ли отменить заявку (только статусы 'new' и 'confirmed')
    if service_request.status not in ['new', 'confirmed']:
        messages.error(request, 'Эту заявку нельзя отменить, так как она уже в работе или выполнена.')
        return redirect('autosalon:profile')
    
    # Если метод POST, отменяем заявку
    if request.method == 'POST':
        # Меняем статус заявки на 'cancelled'
        service_request.status = 'cancelled'
        service_request.save()
        
        messages.success(request, f'Заявка на сервисное обслуживание №{service_request.id} успешно отменена.')
        
        # Здесь можно добавить дополнительную логику, например:
        # - отправка уведомления администратору или сервисному центру
        # - освобождение забронированного времени и т.д.
        
    # Перенаправляем на страницу профиля с активной вкладкой "Сервис"
    return redirect('autosalon:profile')