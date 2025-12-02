"""
URL-конфигурация приложения электронной библиотеки.

Определяет маршруты (URL-шаблоны) для приложения и связывает их
с соответствующими представлениями (views) для обработки запросов.

Структура URL:
    - Начальная страница и навигация
    - Аутентификация и авторизация
    - Управление книгами (CRUD операции)
    - Просмотр и исследование контента
"""

from django.urls import path
from . import views

# Основные URL-маршруты приложения
urlpatterns = [
    # Главная страница приложения (дашборд)
    path('', views.home, name='home'),
    
    # Страница обзора книг по категориям
    path('explore/', views.explore, name='explore'),
    
    # Страница регистрации нового пользователя
    path('register/', views.register, name='register'),
    
    # Страница входа в систему (аутентификация)
    path('login/', views.login, name='login'),
    
    # Добавление новой книги (требует ID пользователя)
    path('addBook/<int:user_id>/', views.addBook, name='addBook'),
    
    # Удаление книги (требует ID книги)
    path('deleteBook/<int:book_id>/', views.deleteBook, name='deleteBook'),
    
    # Редактирование информации о книге (требует ID книги)
    path('editBook/<int:book_id>/', views.editBook, name='editBook'),
    
    # Просмотр детальной информации о книге (требует ID книги)
    path('viewBook/<int:book_id>/', views.viewBook, name='viewBook'),
    
    # Просмотр книг, добавленных конкретным пользователем (требует ID пользователя)
    path('contri/<int:user_id>/', views.contri, name='contri'),
    
    # Выход из системы (завершение сессии)
    path('logout/', views.logout, name='logout')
]