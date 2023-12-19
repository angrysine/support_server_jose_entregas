"""
URL configuration for plataform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from common.views import HomeView, LogsView, LogAPI, AutorizedNumberAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', HomeView.as_view(), name='index'),
    path('logs/', LogsView.as_view(), name='logs'),

    path('api/logs/create/', LogAPI.create_log, name='create_log'),
    path('api/logs/status/', LogAPI.update_status, name='update_status'),
    path('api/number/create/', AutorizedNumberAPI.create_autorized_number, name='create_autorized_number'),
    path('api/number/get/', AutorizedNumberAPI.get_all_autorized_number, name='get_all_autorized_number'),
    path('api/number/delete/', AutorizedNumberAPI.delete_autorized_number, name='delete_autorized_number'),
]
