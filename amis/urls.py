from django.urls import path
from . import views

app_name = 'amis'

urlpatterns = [
    path('list/', views.friend_list, name='friend_list'),
    path('requests/', views.pending_requests, name='pending_requests'),
    path('send/<str:username>/', views.send_request, name='send_request'),
    path('accept/<int:pk>/', views.accept_request, name='accept_request'),
    path('reject/<int:pk>/', views.reject_request, name='reject_request'),
    path('remove/<str:username>/', views.remove_friend, name='remove_friend'),
]
