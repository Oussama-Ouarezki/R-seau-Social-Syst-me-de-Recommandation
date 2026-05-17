from django.urls import path
from . import views

app_name = 'publications'

urlpatterns = [
    path('', views.feed, name='feed'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
]
