''' ФОРМА ДЛЯ ВВОДА СВЕДЕНИЙ О КНИГЕ'''
''' В данном фале определяется форма с полями для названия, аннотации, количества страниц, PDF-файла, категории. Форма использует в оформлении CSS-классы Bootstrap и устанавливает все поля обязательными для отправки.'''

from django import forms
from .models import EBooksModel

class EBookForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('Education', 'Education'),
        ('Fiction', 'Fiction'),
        ('Science', 'Science')
    ]
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)

    class Meta:
        model = EBooksModel
        fields = ['title', 'summary', 'pages', 'pdf', 'category']

    def __init__(self, *args, **kwargs):
        super(EBookForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите название'
        })
        self.fields['summary'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите аннотацию'
        })
        self.fields['pages'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Укажите количество страниц'
        })
        self.fields['pdf'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Скачать PDF'
        })
        self.fields['category'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Выбрать категорию книги'
        })

        for field_name, field in self.fields.items():
            field.required = True
