''' ПРЕДСТАВЛЕНИЯ ПРОЕКТА '''
from django.shortcuts import render, redirect, get_object_or_404
from elibrary_app.models import EBooksModel
from elibrary_app.forms import EBookForm
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# 1. Регистрация (регистрация пользователей)
def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        firstName = request.POST['first-name']
        lastName = request.POST['last-name']

        if User.objects.filter(username=email).exists():
            messages.info(request, 'Пользователь уже зарегистрирован в библиотеке')
            return render(request, 'register.html')
        else:
            register = User.objects.create_user(username=email, password=password, first_name=firstName, last_name=lastName)
            return redirect('login')
    return render(request, 'register.html')

# 2. Вход (аутентификация пользователей)
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)  # Исправлено: authenticate

        if user is not None:
            auth.login(request, user)
            print('Вход выполнен')
            return redirect('home')
        else:
            messages.info(request, 'Некорректные данные для входа')
            return redirect('login')  # Исправлено: redirect вместо render
    else:
        return render(request, 'login.html')
    
# 3. Главная страница (дашборд)
def home(request):
    return render(request, 'home.html')

# 4. Обзор (распределение книг по категориям)
def explore(request):
    edu_books = EBooksModel.objects.filter(category='Education')
    fiction_books = EBooksModel.objects.filter(category='Fiction')
    science_books = EBooksModel.objects.filter(category='Science')
    return render(request, 'explore.html',{
        'edu_books': edu_books,
        'fiction_books': fiction_books,
        'science_books': science_books
    })

# 5. Добавить книгу (добавление новых книг авторизованными пользователями)
@login_required
def addBook(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = EBookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.author = user.first_name + " " + user.last_name
            book.author_id = user.id
            print(book.author)
            book.save()
            print('Книга добавлена')
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = EBookForm()
    return render(request, 'addBook.html', {'form': form})

# 6. Книги пользователя (книги, добавленные данным пользователем)
@login_required
def contri(request, user_id):
    books = EBooksModel.objects.filter(author_id=user_id)
    return render(request, 'contri.html', {'books': books})

# 10. Выход (окончание сессии пользователя)
def logout(request):
    auth.logout(request)
    return redirect('home')  # Исправлено: redirect вместо render

# 8. Удалить книгу (удаление добавленной книги)
@login_required
def deleteBook(request, book_id):
    book = get_object_or_404(EBooksModel, id=book_id)
    book.delete()
    return redirect('home')  # Исправлено: redirect вместо render

# 7. Редактирование книги (изменение информации о добавленной книге)
@login_required
def editBook(request, book_id):
    book = get_object_or_404(EBooksModel, id=book_id)
    if request.method == 'POST':
        form = EBookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            print('Данные о книге изменены')
            return redirect('contri', user_id=request.user.id)
        else:
            print(form.errors)
    else:
        form = EBookForm(instance=book)
    return render(request, 'editBook.html', {
        'form': form,
        'book': book
    })

# 9. Просмотр книги (информация о книге и возможность её скачать/просмотреть)
def viewBook(request, book_id):
    book = get_object_or_404(EBooksModel, id=book_id)
    book.summary = book.summary.replace('\n', '<br/>')
    return render(request, 'viewBook.html', {'book': book})