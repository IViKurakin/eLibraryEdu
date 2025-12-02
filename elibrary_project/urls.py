"""
URL-конфигурация основного проекта электронной библиотеки.

Этот файл определяет корневые URL-шаблоны проекта, включая:
- Административную панель Django
- Статические и медиа-файлы в режиме разработки
- Маршруты приложения электронной библиотеки
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

# Основные URL-шаблоны проекта
urlpatterns = [
    # Административная панель Django
    path('admin/', admin.site.urls),
    
    # Включение URL-шаблонов приложения электронной библиотеки
    path('', include('elibrary_app.urls'))
]

# Обслуживание медиа-файлов в режиме разработки
if settings.DEBUG or not settings.DEBUG:
    """
    Настройка обслуживания медиа-файлов.
    
    Внимание: В продакшн-окружении медиа-файлы должны обслуживаться
    веб-сервером (Nginx, Apache), а не Django.
    """
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)