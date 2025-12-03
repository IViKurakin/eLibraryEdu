import pytest
from django.urls import reverse
from elibrary_app.tests.factories import UserFactory, EBookFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User 
from elibrary_app.models import EBooksModel

@pytest.mark.django_db
class TestAuthViews:
    def test_register_get(self, client):
        response = client.get(reverse("register"))
        assert response.status_code == 200

    def test_register_post_success(self, client):
        data = {
            "email": "newuser@test.com",
            "password": "supersecret123",
            "first-name": "Иван",
            "last-name": "Иванов",
        }
        response = client.post(reverse("register"), data)
        assert response.status_code == 302
        assert response.url == reverse("login")
        assert User.objects.filter(username="newuser@test.com").exists()

    def test_register_post_user_exists(self, client):
        UserFactory(username="exists@test.com")
        data = {
            "email": "exists@test.com",
            "password": "pass123",
            "first-name": "A",
            "last-name": "B",
        }
        response = client.post(reverse("register"), data)
        assert response.status_code == 200
        
        assert "Пользователь уже зарегистрирован в библиотеке" in response.content.decode("utf-8")

    def test_login_get(self, client):
        response = client.get(reverse("login"))
        assert response.status_code == 200

    def test_login_success(self, client):
        user = UserFactory(username="login@test.com")
        user.set_password("testpass123")
        user.save()

        response = client.post(reverse("login"), {
            "email": "login@test.com",
            "password": "testpass123",
        })
        assert response.status_code == 302
        assert response.url == reverse("home")
        assert "_auth_user_id" in client.session

    def test_login_fail(self, client):
        response = client.post(reverse("login"), {
            "email": "wrong@wrong.com",
            "password": "wrong",
        }, follow=True)  

        assert response.status_code == 200
        assert "Некорректные данные для входа" in response.content.decode("utf-8")


@pytest.mark.django_db
class TestBookViews:
    @pytest.fixture
    def logged_client(self, client):
        user = UserFactory()
        client.force_login(user)
        return client, user

    def test_home(self, client):
        response = client.get(reverse("home"))
        assert response.status_code == 200

    def test_explore(self, client):
        EBookFactory.create_batch(3, category="Education")
        EBookFactory.create_batch(2, category="Fiction")
        EBookFactory(category="Science")
        response = client.get(reverse("explore"))
        assert response.status_code == 200
        assert len(response.context["edu_books"]) == 3
        assert len(response.context["fiction_books"]) == 2
        assert len(response.context["science_books"]) == 1

    def test_add_book_get(self, logged_client):
        client, user = logged_client
        url = reverse("addBook", args=[user.id])
        response = client.get(url)
        assert response.status_code == 200

    def test_add_book_post_success(self, logged_client):
        client, user = logged_client
        url = reverse("addBook", args=[user.id])
        pdf_file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
        data = {
            "title": "Тестовая книга",
            "summary": "Аннотация книги",
            "pages": "350",
            "pdf": pdf_file,
            "category": "Fiction",
            "author": "",  
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert response.url == reverse("home")

        book = EBooksModel.objects.first()
        assert book.title == "Тестовая книга"
        assert book.author == f"{user.first_name} {user.last_name}"
        assert book.author_id == user.id

    def test_contri_view(self, logged_client):
        client, user = logged_client
        EBookFactory.create_batch(4, set_author_data=user)
        EBookFactory()  
        url = reverse("contri", args=[user.id])
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.context["books"]) == 4

    def test_delete_book(self, logged_client):
        client, user = logged_client
        book = EBookFactory(set_author_data=user)
        url = reverse("deleteBook", args=[book.id])
        response = client.get(url)  
        assert response.status_code == 302
        assert not EBooksModel.objects.filter(id=book.id).exists()

    def test_edit_book(self, logged_client):
        client, user = logged_client
        book = EBookFactory(set_author_data=user, title="Старая книга")
        url = reverse("editBook", args=[book.id])
        pdf2 = SimpleUploadedFile("new.pdf", b"new_content", content_type="application/pdf")
        data = {
            "title": "Новое название",
            "summary": "Новое описание",
            "pages": "500",
            "pdf": pdf2,
            "category": "Science",
        }
        response = client.post(url, data)
        assert response.status_code == 302
        book.refresh_from_db()
        assert book.title == "Новое название"

    def test_view_book(self, client):
        book = EBookFactory(title="Книга для просмотра", summary="Первая строка\nВторая строка")
        url = reverse("viewBook", args=[book.id])
        response = client.get(url)
        assert response.status_code == 200
        content = response.content.decode("utf-8")
        assert "<br/>" in content or "<br>" in content  

    def test_logout(self, logged_client):
        client, _ = logged_client
        response = client.get(reverse("logout"))
        assert response.status_code == 302
        assert "_auth_user_id" not in client.session