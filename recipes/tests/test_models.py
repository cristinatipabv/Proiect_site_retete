import pytest
from recipes.models import Book
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_book_creation():
    book = Book.objects.create(
        title="Test book 1",
        content="Test content here 1",
        author="Author Test",
    )

    assert book.title == "Test book 1"
    assert book.content == "Test content here 1"


@pytest.mark.django_db
def test_book_creation_with_user():
    user = User.objects.create(username="test1")
    book = Book.objects.create(
        title="Test book 1",
        content="Test content here 1",
        author="Author Test",
        user=user
    )

    book2 = Book.objects.create(
        title="Test book 2",
        content="Test content here 2",
        author="Author Test2",
        user=user
    )

    assert book.title == "Test book 1"
    assert book.content == "Test content here 1"
    assert book.user.username == "test1"
    assert len(user.books.all()) == 2




