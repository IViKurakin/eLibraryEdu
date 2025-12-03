import pytest
from elibrary_app.tests.factories import EBookFactory

@pytest.mark.django_db
def test_ebook_str():
    book = EBookFactory(title="Война и мир")
    assert str(book) == "Война и мир"

@pytest.mark.django_db
def test_book_pdf_upload_to():
    book = EBookFactory()
    assert book.pdf.name.startswith("pdfs/")
    assert book.pdf.name.endswith(".pdf")