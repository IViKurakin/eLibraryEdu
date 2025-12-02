"""
Основные настройки проекта электронной библиотеки.

Содержит конфигурационные параметры Django-проекта:
- Безопасность и отладка
- Установленные приложения и middleware
- Настройки базы данных
- Языковые и временные параметры
- Статические и медиа-файлы
"""

import os
from pathlib import Path

# Базовый путь к директории проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ для криптографической подписи
# ВНИМАНИЕ: В продакшене должен быть заменен на случайную строку и храниться в безопасности
SECRET_KEY = 'django-insecure-5$rj=n&2_!=+tgvh%e^2o$32m)-wi3a0*=fnvb5i+@5*00=zlh'

# Режим отладки - В продакшене должен быть установлен в False
DEBUG = True

# Разрешенные хосты - в продакшене нужно указать реальные домены
ALLOWED_HOSTS = []

# Установленные приложения проекта
INSTALLED_APPS = [
    'django.contrib.admin',          # Админ-панель Django
    'django.contrib.auth',           # Система аутентификации
    'django.contrib.contenttypes',   # Система типов контента
    'django.contrib.sessions',       # Система сессий
    'django.contrib.messages',       # Система сообщений
    'django.contrib.staticfiles',    # Обработка статических файлов
    'elibrary_app'                   # Пользовательское приложение электронной библиотеки
]

# Промежуточное программное обеспечение (Middleware)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',          # Безопасность
    'django.contrib.sessions.middleware.SessionMiddleware',   # Управление сессиями
    'django.middleware.common.CommonMiddleware',              # Общие функции
    'django.middleware.csrf.CsrfViewMiddleware',              # Защита от CSRF-атак
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Аутентификация
    'django.contrib.messages.middleware.MessageMiddleware',   # Сообщения
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Защита от clickjacking
]

# Корневая конфигурация URL
ROOT_URLCONF = 'elibrary_project.urls'

# Настройки шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Директория с шаблонами проекта
        'APP_DIRS': True,                  # Поиск шаблонов в приложениях
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI приложение для развертывания
WSGI_APPLICATION = 'elibrary_project.wsgi.application'

# Настройки базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Движок базы данных (SQLite)
        'NAME': BASE_DIR / 'db.sqlite3',         # Путь к файлу базы данных
    }
}

# Валидаторы паролей для повышения безопасности
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # Проверка схожести с данными пользователя
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # Проверка минимальной длины
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # Проверка на распространенные пароли
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # Проверка на чисто числовые пароли
    },
]

# Языковые и временные настройки
LANGUAGE_CODE = 'ru-ru'    # Язык интерфейса - русский
TIME_ZONE = 'UTC'          # Часовой пояс (Всемирное координированное время)
USE_I18N = True            # Включение интернационализации
USE_TZ = True              # Использование временных зон

# Настройки статических файлов (CSS, JavaScript, изображения)
STATIC_URL = '/static/'    # URL-префикс для статических файлов
STATICFILES_DIRS = [BASE_DIR / 'static']  # Дополнительные директории со статическими файлами

# Настройки медиа-файлов (загружаемые пользователями - PDF книги)
MEDIA_URL = '/media/'      # URL-префикс для медиа-файлов
MEDIA_ROOT = BASE_DIR / 'media'  # Директория для хранения медиа-файлов

# Автоматическое поле для первичных ключей моделей
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'