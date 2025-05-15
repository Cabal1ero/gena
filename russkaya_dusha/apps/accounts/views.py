from django.shortcuts import render
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.orders.models import CarOrder
from apps.service.models import ServiceRequest
from django.shortcuts import render, redirect

# Create your views here.
class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone = forms.CharField(required=False)
    avatar = forms.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        
        if commit:
            user.save()
            
            # Создаем или обновляем профиль пользователя
            profile, created = UserProfile.objects.get_or_create(user=user)
            if self.cleaned_data.get('phone'):
                profile.phone = self.cleaned_data['phone']
            if self.cleaned_data.get('avatar'):
                profile.avatar = self.cleaned_data['avatar']
            profile.save()
            
        return user
    

def auth(request):
    register_form = UserRegistrationForm()
    login_form = AuthenticationForm()
    
    if request.method == 'POST':
        # Определяем, какая форма была отправлена
        form_type = request.POST.get('form_type')
        
        if form_type == 'register':
            # Важно: передаем request.FILES для обработки загруженных файлов
            register_form = UserRegistrationForm(request.POST, request.FILES)
            if register_form.is_valid():
                user = register_form.save()
                
                # Обработка аватара - это уже должно быть в методе save() формы UserRegistrationForm
                # Но можно добавить дополнительную логику здесь при необходимости
                
                # Автоматически входим пользователя после регистрации
                username = register_form.cleaned_data.get('username')
                password = register_form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(request, f'Аккаунт создан успешно! Добро пожаловать, {user.first_name}!')
                return redirect('autosalon:home')
        else:
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f'Добро пожаловать, {user.first_name if user.first_name else user.username}!')
                    return redirect('autosalon:home')
    
    return render(request, 'registration/auth.html', {
        'register_form': register_form,
        'login_form': login_form
    })

@login_required
def profile_dashboard(request):
    """Отображение личного кабинета пользователя"""
    service_requests = ServiceRequest.objects.filter(user=request.user)
    orders = CarOrder.objects.filter(user=request.user)
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
        if action == 'update_profile':
            user = request.user
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')
            user.save()
            profile = user.account_profile
            profile.phone = request.POST.get('phone', '')
            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
            if request.POST.get('remove_avatar') == 'true':
                profile.avatar = None
            profile.save()
            messages.success(request, 'Профиль успешно обновлен!')
        elif action == 'change_password':
            old_password = request.POST.get('old_password', '')
            new_password1 = request.POST.get('new_password1', '')
            new_password2 = request.POST.get('new_password2', '')
            if not request.user.check_password(old_password):
                messages.error(request, 'Неверный текущий пароль.')
                return redirect('accounts:profile')
            if new_password1 != new_password2:
                messages.error(request, 'Новые пароли не совпадают.')
                return redirect('accounts:profile')
            if len(new_password1) < 4:
                messages.error(request, 'Пароль должен содержать не менее 4 символов.')
                return redirect('accounts:profile')
            request.user.set_password(new_password1)
            request.user.save()
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Пароль успешно изменен!')
        return redirect('accounts:profile')
    return redirect('accounts:profile')
