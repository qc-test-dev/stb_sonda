"""stb_sonda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from .views import home, connect_device, live_view, proxy_to_ws_scrcpy
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', home, name='home'),
    path('connect/<str:ip>/', connect_device, name='connect_device'),
    path('live/<str:ip>/', live_view, name='live_view'),
    path('stream/<str:ip_port>/', proxy_to_ws_scrcpy, name='proxy_to_ws_scrcpy'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
