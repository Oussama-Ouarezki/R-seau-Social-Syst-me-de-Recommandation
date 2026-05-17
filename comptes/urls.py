from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'comptes'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='comptes/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='comptes/logout.html'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<str:username>/', views.profile_view, name='profile_detail'),
]
