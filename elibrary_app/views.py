"""
Представления (views) приложения электронной библиотеки.

Этот модуль содержит все представления Django для обработки
HTTP-запросов в приложении электронной библиотеки. Включает функции
для регистрации, аутентификации, управления книгами и навигации.
"""

from django.shortcuts import render, redirect, get_object_or_404
from elibrary_app.models import EBooksModel
from elibrary_app.forms import EBookForm
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def register(request):
    """
    Обработка регистрации новых пользователей.
    
    Args:
        request (HttpRequest): Объект HTTP-запроса
        
    Returns:
        HttpResponse: Страница регистрации или перенаправление на страницу входа
        
    Функционал:
        - Проверяет существование пользователя с указанным email
        - Создает нового пользователя при успешной проверке
        - Отображает сообщения об ошибках при конфликтах
    """
    if request.method == 'POST':
        # Получение данных из формы регистрации
        email = request.POST['email']
        password = request.POST['password']
        firstName = request.POST['first-name']
        lastName = request.POST['last-name']

        # Проверка существования пользователя с таким email
        if User.objects.filter(username=email).exists():
            messages.info(request, 'Пользователь уже зарегистрирован в библиотеке')
            return render(request, 'register.html')
        else:
            # Создание нового пользователя
            register = User.objects.create_user(
                username=email, 
                password=password, 
                first_name=firstName, 
                last_name=lastName
            )
            return redirect('login')
    
    # Отображение формы регистрации для GET-запросов
    return render(request, 'register.html')


def login(request):
    """
    Обработка аутентификации пользователей.
    
    Args:
        request (HttpRequest): Объект HTTP-запроса
        
    Returns:
        HttpResponse: Страница входа или перенаправление на главную страницу
        
    Функционал:
        - Проверяет учетные данные пользователя
        - Выполняет вход при успешной аутентификации
        - Отображает сообщения об ошибках при неверных данных
    """
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Аутентификация пользователя
        user = auth.authenticate(username=email, password=password)

        if user is not None:
            # Успешная аутентификация - вход в систему
            auth.login(request, user)
            print('Вход выполнен')
            return redirect('home')
        else:
            # Неверные учетные данные
            messages.info(request, 'Некорректные данные для входа')
            return redirect('login')
    else:
        # Отображение формы входа для GET-запросов
        return render(request, 'login.html')
    

def home(request):
    """
    Отображение главной страницы (дашборда).
    
    Args:
        request (HttpRequest): Объект HTTP-запроса
        
    Returns:
        HttpResponse: Главная страница приложения
    """
    return render(request, 'home.html')


def explore(request):
    """
    Отображение страницы обзора книг по категориям.
    
    Args:
        request (HttpRequest): Объект HTTP-запроса
        
    Returns:
        HttpResponse: Страница с книгами, распределенными по категориям
        
    Категории:
        - Education: учебная литература
        - Fiction: художественная литература  
        - Science: научная литература
    """
    # Получение книг по категориям
    edu_books = EBooksModel.objects.filter(category='Education')
    fiction_books = EBooksModel.objects.filter(category='Fiction')
    science_books = EBooksModel.objects.filter(category='Science')
    
    return render(request, 'explore.html', {
        'edu_books': edu_books,
        'fiction_books': fiction_books,
        'science_books': science_books
    })


@login_required
def addBook(request, user_id):
    """
    Добавление новой книги в библиотеку.
    
    Args:
        request (HttpRequest): Объект HTTP-запроса
        user_id (int): Идентификатор пользователя, добавляющего книгу
        
    Returns:
        HttpResponse: Страница добавления книги или перенаправление на главную
        
    Требования:
        - Только для авторизованных пользователей
        - Пользователь должен иметь права на добавление книг
    """
    # Получение объекта пользователя
    user = User.objects.get(id=user_id)
    
    if request.method == 'POST':
        # Создание формы с данными из запроса
        form = EBookForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Сохранение книги с указанием автора
            book = form.save(commit=False)
            book.author = f"{user.first_name} {user.last_name}"
            book.author_id = user.id
            print(book.author)
            book.save()
            print('Книга добавлена')
            return redirect('home')
        else:
            # Вывод ошибок валидации формы
            print(form.errors)
    else:
        # Создание пустой формы для GET-запроса
        form = EBookForm()
    
    return render(request, 'addBook.html', {'form': form})


@login_required
def contri(request, user_id):
    """
    Просмотр книг, добавленных конкретным пользователем.
    
    Args:
        request (HttpRequest): Объект HTTP-запроса
        user_id (int): Идентификатор пользователя
        
    Returns:
        HttpResponse: Страница со списком книг пользователя
    """
    # Фильтрация книг по автору
    books = EBooksModel.objects.filter(author_id=user_id)
    return render(request, 'contri.html', {'books': books})


def logout(request):
    """
    Выход пользователя из системы.
    
    Args:
        request (HttpRequest): Объект HTTP-запроса
        
    Returns:
        HttpResponse: Перенаправление на главную страницу
    """
    # Завершение сессии пользователя
    auth.logout(request)
    return redirect('home')


@login_required
def deleteBook(request, book_id):
    """
    Удаление книги из библиотеки.
    
    Args:
        request (HttpRequest): Объект HTTP-запроса
        book_id (int): Идентификатор удаляемой книги
        
    Returns:
        HttpResponse: Перенаправление на главную страницу
        
    Примечание:
        - Только автор книги или администратор могут удалять книги
        - Операция необратима
    """
    # Получение книги или возврат 404 ошибки
    book = get_object_or_404(EBooksModel, id=book_id)
    
    # Удаление книги из базы данных
    book.delete()
    return redirect('home')


@login_required
def editBook(request, book_id):
    """
    Редактирование информации о книге.
    
    Args:
        request (HttpRequest): Объект HTTP-запроса
        book_id (int): Идентификатор редактируемой книги
        
    Returns:
        HttpResponse: Страница редактирования или перенаправление на страницу книг пользователя
    """
    # Получение книги для редактирования
    book = get_object_or_404(EBooksModel, id=book_id)
    
    if request.method == 'POST':
        # Создание формы с данными и прикрепленным файлом
        form = EBookForm(request.POST, request.FILES, instance=book)
        
        if form.is_valid():
            # Сохранение изменений
            form.save()
            print('Данные о книге изменены')
            return redirect('contri', user_id=request.user.id)
        else:
            # Вывод ошибок валидации
            print(form.errors)
    else:
        # Создание формы с текущими данными книги
        form = EBookForm(instance=book)
    
    return render(request, 'editBook.html', {
        'form': form,
        'book': book
    })


def viewBook(request, book_id):
    """
    Просмотр детальной информации о книге.
    
    Args:
        request (HttpRequest): Объект HTTP-запроса
        book_id (int): Идентификатор просматриваемой книги
        
    Returns:
        HttpResponse: Страница с полной информацией о книге
        
    Особенности:
        - Преобразует переносы строк в аннотации в HTML-теги <br/>
        - Предоставляет ссылки для скачивания PDF-файла
    """
    # Получение книги из базы данных
    book = get_object_or_404(EBooksModel, id=book_id)
    
    # Форматирование аннотации для HTML-отображения
    book.summary = book.summary.replace('\n', '<br/>')
    
    return render(request, 'viewBook.html', {'book': book})