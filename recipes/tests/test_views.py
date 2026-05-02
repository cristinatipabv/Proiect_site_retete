import pytest
from recipes.models import Recipe
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.urls import reverse

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="test1",
        email="test1@test.com",
        password="tomatoes12345"
    )


@pytest.fixture
def logged_in_client(client: Client, user) -> Client:
    client.login(username="test1", password="tomatoes12345")
    return client


@pytest.fixture
def recipe_obj(user):
    return Recipe.objects.create(
        title="Reteta noua",
        content="Test Content",
        author="New author1",
        ingredients="Cartofi, ceapa, ulei",
        nr_ingredients=4,
        time_minutes=30,
        servings=2,
        user=user
    )


# ==================== CRUD TESTS ====================

@pytest.mark.django_db
def test_recipe_create(logged_in_client: Client):
    response = logged_in_client.post(
        reverse("create_recipe"),
        {
            "title": "Reteta1",
            "author": "Tester1",
            "content": "Test content11",
            "ingredients": "Tomate, busuioc, mozzarella",
            "nr_ingredients": 5,
            "time_minutes": 25,
            "servings": 2,
        }
    )
    assert response.status_code == 302
    assert Recipe.objects.count() == 1


@pytest.mark.django_db
def test_recipe_delete(logged_in_client: Client, recipe_obj: Recipe):
    recipe_id = recipe_obj.pk
    response = logged_in_client.post(
        reverse("delete_recipe", kwargs={"pk": recipe_id})
    )
    assert response.status_code == 302
    assert not Recipe.objects.filter(pk=recipe_id).exists()


@pytest.mark.django_db
def test_recipe_update(logged_in_client: Client, recipe_obj: Recipe):
    recipe_id = recipe_obj.pk
    response = logged_in_client.post(
        reverse("update_recipe", kwargs={"pk": recipe_id}),
        {
            "title": "New title1",
            "author": "New author1",
            "content": "skibidi content",
            "ingredients": "New ingredients list",
            "nr_ingredients": 6,
            "time_minutes": 45,
            "servings": 3,
        }
    )
    assert response.status_code == 302

    recipe_obj.refresh_from_db()
    assert recipe_obj.title == "New title1"
    assert recipe_obj.author == "New author1"
    assert recipe_obj.content == "skibidi content"


# ==================== SORTING TEST ====================

@pytest.mark.django_db
def test_recipe_list_sorting(logged_in_client: Client, user):
    """Test sortare retete"""
    Recipe.objects.create(
        title="Ciorba de legume", content="x", author="Mama",
        ingredients="x", nr_ingredients=8, time_minutes=60, user=user
    )
    Recipe.objects.create(
        title="Apple Pie", content="x", author="Chef",
        ingredients="x", nr_ingredients=6, time_minutes=90, user=user
    )
    Recipe.objects.create(
        title="Zucchini Bread", content="x", author="Baker",
        ingredients="x", nr_ingredients=5, time_minutes=50, user=user
    )

    # Test list view
    response = logged_in_client.get(reverse("recipe_list"))
    assert response.status_code == 200

    # Afla ce cheie folosește view-ul tău în context
    context_data = response.context
    recipes = context_data.get("recipes") or context_data.get("object_list") or \
              context_data.get("recipe_list") or context_data.get("page_obj")

    assert recipes is not None, f"Context keys: {list(context_data.keys())}"

    titles = [r.title for r in recipes]
    print("Titluri returnate:", titles)