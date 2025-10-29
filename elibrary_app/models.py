''' МОДЕЛИ ПРОЕКТА '''
'''
Модели с полями для названий книг, аннотаций, количества страниц, загрузки PDF-файлов, имени автора, категории и идентификатора.
Модели позволяют хранить и извлекать информацию о книгах.
'''

from django.db import models

class EBooksModel(models.Model):
    title = models.CharField(max_length=150)
    summary = models.TextField(max_length=2000)
    pages = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='pdfs/')
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=300)
    author_id = models.IntegerField(default=0)
    
    # Метод __str__() класса EBooksModel определяет строковое представление экземпляра, возвращая название книги
    def __str__(self):
        return f"{self.title}"