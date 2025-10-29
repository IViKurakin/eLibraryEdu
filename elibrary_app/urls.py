''' ШАБЛОНЫ URL '''
''' В данном файле определяются шаблоны URL-адресов в приложении Django, связывающие определенные пути с соответствующими представлениями (views) '''

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('explore/', views.explore, name='explore'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('addBook/<int:user_id>/', views.addBook, name='addBook'),
    path('deleteBook/<int:book_id>/', views.deleteBook, name='deleteBook'),  # Исправлено: book_id
    path('editBook/<int:book_id>/', views.editBook, name='editBook'),  # Исправлено: book_id
    path('viewBook/<int:book_id>/', views.viewBook, name='viewBook'),  # Исправлено: book_id
    path('contri/<int:user_id>/', views.contri, name='contri'),
    path('logout/', views.logout, name='logout')
]