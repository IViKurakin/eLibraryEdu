"""
Формы приложения электронной библиотеки.

Определяет форму для ввода сведений о книге с полями:
- Название книги
- Аннотация
- Количество страниц  
- PDF-файл
- Категория

Форма использует CSS-классы Bootstrap для оформления и устанавливает
все поля обязательными для отправки.
"""

from django import forms
from .models import EBooksModel


class EBookForm(forms.ModelForm):
    """
    Форма для добавления и редактирования электронных книг.
    
    Поля формы:
        - title: название книги (CharField)
        - summary: аннотация (TextField)
        - pages: количество страниц (CharField)
        - pdf: PDF-файл книги (FileField)
        - category: категория книги (ChoiceField)
        
    Валидация:
        - Все поля обязательны для заполнения
        - PDF-файл должен быть в формате PDF
        - Категория выбирается из предопределенного списка
    """
    
    # Определение категорий для выпадающего списка
    CATEGORY_CHOICES = [
        ('Education', 'Education'),    # Учебная литература
        ('Fiction', 'Fiction'),        # Художественная литература
        ('Science', 'Science')         # Научная литература
    ]
    
    # Поле выбора категории с предопределенными вариантами
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)

    class Meta:
        """
        Мета-класс для настройки формы.
        
        Определяет:
            - model: модель, с которой связана форма
            - fields: поля модели, включаемые в форму
            - widgets: дополнительные настройки виджетов полей
        """
        model = EBooksModel
        fields = ['title', 'summary', 'pages', 'pdf', 'category']

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы с настройками виджетов.
        
        Настраивает:
            - CSS-классы для всех полей (form-control Bootstrap)
            - Placeholder-текст для подсказок пользователям
            - Обязательность заполнения всех полей
        """
        super(EBookForm, self).__init__(*args, **kwargs)

        # Настройка поля "Название"
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',              # Bootstrap класс
            'placeholder': 'Введите название'     # Текст-подсказка
        })
        
        # Настройка поля "Аннотация"
        self.fields['summary'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите аннотацию'
        })
        
        # Настройка поля "Количество страниц"
        self.fields['pages'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Укажите количество страниц'
        })
        
        # Настройка поля "PDF-файл"
        self.fields['pdf'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Скачать PDF'
        })
        
        # Настройка поля "Категория"
        self.fields['category'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Выбрать категорию книги'
        })

        # Установка обязательности всех полей формы
        for field_name, field in self.fields.items():
            field.required = True