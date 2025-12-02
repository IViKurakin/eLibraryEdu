"""
Конфигурация административной панели Django.

Регистрирует модели приложения электронной библиотеки
в административной панели Django для управления данными.
"""

from django.contrib import admin
from .models import EBooksModel

# Регистрация модели EBooksModel в административной панели
admin.site.register(EBooksModel)