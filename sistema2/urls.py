# sistema2/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from api import views  # Certifique-se de importar as views da aplicação

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', views.index, name='index'),  # Página inicial
    path('', lambda request: redirect('login', permanent=False)),  # <- redireciona para login
    path('api/', include('api.urls')),    # Inclui as URLs da API
]
