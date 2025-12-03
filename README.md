# eLibraryEdu

# Техническая документация проекта "Электронная библиотека"

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.x-green.svg)](https://djangoproject.com)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/yourusername/elibrary)

## 1. Общее описание

**Электронная библиотека** — веб-приложение на Django для хранения и управления электронными книгами в формате PDF. Пользователи могут регистрироваться, добавлять книги, просматривать каталог и управлять своими книгами.

## 2. Структура проекта

```
elibrary/
├── elibrary_app/                    # Основное приложение
│   ├── migrations/                  # Миграции базы данных
│   ├── admin.py                    # Админ-панель
│   ├── forms.py                    # Формы для книг
│   ├── models.py                   # Модели данных
│   ├── urls.py                     # Маршруты приложения
│   └── views.py                    # Контроллеры
├── elibrary_project/               # Настройки проекта
│   ├── media/                      # Загружаемые файлы
│   │   └── pdfs/                   # PDF книги
│   ├── settings.py                 # Настройки Django
│   ├── urls.py                     # Корневые маршруты
│   └── wsgi.py                     # WSGI конфигурация
├── static/                         # CSS, JS файлы
│   └── css/
│       └── style.css              # Основные стили
├── templates/                      # HTML шаблоны
│   ├── base.html                  # Базовый шаблон
│   ├── home.html                  # Главная страница
│   ├── explore.html               # Все книги
│   ├── viewBook.html              # Детали книги
│   ├── login.html                 # Вход
│   ├── register.html              # Регистрация
│   ├── addBook.html               # Добавить книгу
│   ├── editBook.html              # Редактировать книгу
│   └── contri.html                # Мои книги
├── db.sqlite3                     # База данных
└── manage.py                      # Команды Django
```

## 3. Быстрый старт

### Установка и запуск

1. **Создайте виртуальное окружение:**
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

2. **Установите Django:**
```bash
pip install django
```

3. **Настройте базу данных:**
```bash
python manage.py migrate
```

4. **Создайте суперпользователя:**
```bash
python manage.py createsuperuser
```

5. **Запустите сервер:**
```bash
python manage.py runserver
```

6. **Откройте в браузере:**
- Главная страница: http://localhost:8000
- Админ-панель: http://localhost:8000/admin

## 4. Модель данных

### Модель книги (EBooksModel)

```python
# elibrary_app/models.py
class EBooksModel(models.Model):
    title = models.CharField(max_length=150)      # Название
    summary = models.TextField(max_length=2000)   # Описание
    pages = models.CharField(max_length=100)      # Страницы
    pdf = models.FileField(upload_to='pdfs/')     # PDF файл
    author = models.CharField(max_length=100)     # Имя автора
    category = models.CharField(max_length=300)   # Категория
    author_id = models.IntegerField(default=0)    # ID пользователя
    
    def __str__(self):
        return self.title
```

### Категории книг:
- `Education` - Учебная литература
- `Fiction` - Художественная литература
- `Science` - Научная литература

## 5. URL маршруты

### Основные маршруты:

| URL | Описание | Доступ |
|-----|----------|--------|
| `/` | Главная страница | Все |
| `/explore/` | Все книги по категориям | Все |
| `/register/` | Регистрация | Все |
| `/login/` | Вход | Все |
| `/logout/` | Выход | Все |
| `/addBook/<user_id>/` | Добавить книгу | Только авторизованные |
| `/viewBook/<book_id>/` | Просмотр книги | Все |
| `/editBook/<book_id>/` | Редактировать книгу | Только автор |
| `/deleteBook/<book_id>/` | Удалить книгу | Только автор |
| `/contri/<user_id>/` | Мои книги | Только автор |

## 6. Представления (Views)

### Основные функции:

1. **Регистрация (`register`)**
   - Создает нового пользователя
   - Проверяет уникальность email
   - Перенаправляет на страницу входа

2. **Вход (`login`)**
   - Проверяет логин и пароль
   - Создает сессию пользователя
   - Перенаправляет на главную

3. **Добавление книги (`addBook`)**
   - Только для авторизованных пользователей
   - Сохраняет PDF файл в `media/pdfs/`
   - Привязывает книгу к автору

4. **Просмотр книг (`explore`)**
   - Показывает книги по категориям
   - Доступно всем пользователям

5. **Управление книгами**
   - Редактирование и удаление доступно только автору книги
   - Использует декоратор `@login_required`

## 7. Формы

### Форма для книг (EBookForm)

```python
# elibrary_app/forms.py
class EBookForm(forms.ModelForm):
    category = forms.ChoiceField(choices=[
        ('Education', 'Education'),
        ('Fiction', 'Fiction'),
        ('Science', 'Science')
    ])
    
    class Meta:
        model = EBooksModel
        fields = ['title', 'summary', 'pages', 'pdf', 'category']
```

## 8. Администрирование

### Панель администратора:
- Доступна по адресу: `/admin/`
- Логин и пароль от суперпользователя
- Управление книгами и пользователями

### Регистрация модели в админке:
```python
# elibrary_app/admin.py
from django.contrib import admin
from .models import EBooksModel

admin.site.register(EBooksModel)
```

## 9. Настройки (settings.py)

### Основные настройки:

```python
# elibrary_project/settings.py

# Безопасность (для разработки)
SECRET_KEY = 'ваш-секретный-ключ'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# База данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Статические файлы
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Медиа файлы
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

## 10. Решение проблем

### Частые ошибки и решения:

1. **"No module named 'elibrary_app'"**
   - Проверьте, что приложение добавлено в `INSTALLED_APPS`:
   ```python
   INSTALLED_APPS = [
       # ...
       'elibrary_app',
   ]
   ```

2. **"TemplateDoesNotExist"**
   - Проверьте путь к шаблонам в `settings.py`:
   ```python
   TEMPLATES = [
       {
           'DIRS': [BASE_DIR / 'templates'],
           # ...
       },
   ]
   ```

3. **Ошибка с медиа-файлами**
   - Убедитесь, что в `urls.py` есть:
   ```python
   if settings.DEBUG:
       urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   ```

4. **Ошибка миграций**
   - Удалите файлы в `migrations/` (кроме `__init__.py`)
   - Удалите `db.sqlite3`
   - Выполните:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

---

**Версия документации:** 1.0  
**Последнее обновление:** Декабрь 2025
