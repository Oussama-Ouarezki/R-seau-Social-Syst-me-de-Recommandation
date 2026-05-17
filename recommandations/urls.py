from django.urls import path
from . import views

app_name = 'recommandations'

urlpatterns = [
    path('friends/', views.friend_recommendations, name='friend_recommendations'),
    path('content/', views.content_recommendations, name='content_recommendations'),
]
