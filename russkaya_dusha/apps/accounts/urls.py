
from django.urls import path, include
from views import *

urlspatterns= [
    path('auth/', views.auth, name='auth'),  # Используем имя функции auth вместо auth_view
    path('profile/', views.profile_dashboard, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'), 
]