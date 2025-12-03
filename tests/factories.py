import factory
from django.contrib.auth.models import User
from elibrary_app.models import EBooksModel
from django.core.files.uploadedfile import SimpleUploadedFile

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Faker("email")
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        user = User.objects.create_user(
            username=kwargs.get("username"),
            email=kwargs.get("email"),
            password="testpass123",
            first_name=kwargs.get("first_name"),
            last_name=kwargs.get("last_name"),
        )
        return user


class EBookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EBooksModel
    title = factory.Faker("sentence", nb_words=4)
    summary = factory.Faker("paragraph", nb_sentences=5)
    pages = factory.Faker("random_int", min=50, max=1200)
    pdf = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
    author = factory.Faker("name")
    category = factory.Iterator(["Education", "Fiction", "Science", "Other"])

    @factory.post_generation
    def set_author_data(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:  
            user = extracted
            self.author = f"{user.first_name} {user.last_name}"
            self.author_id = user.id
        else:
            pass