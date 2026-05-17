"""
URL configuration for reseau_social project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('comptes/', include('comptes.urls')),
    path('publications/', include('publications.urls')),
    path('amis/', include('amis.urls')),
    path('recommandations/', include('recommandations.urls')),
    
    # Redirection racine vers le fil d'actu ou login
    path('', lambda request: redirect('publications:feed') if request.user.is_authenticated else redirect('comptes:login'), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
