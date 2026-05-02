import pytest
from recipes.models import Recipe
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_recipe_creation():
    """Test crearea simplă a unei rețete"""
    recipe = Recipe.objects.create(
        title="Testare reteta",
        content="Test content here 1",
        author="Author Test",
        ingredients="Cartofi, ceapa, ulei, sare",
        nr_ingredients=4,
        time_minutes=30,
        servings=2,
    )

    assert recipe.title == "Testare reteta"
    assert recipe.content == "Test content here 1"
    assert recipe.author == "Author Test"
    assert recipe.ingredients == "Cartofi, ceapa, ulei, sare"
    assert recipe.nr_ingredients == 4
    assert recipe.time_minutes == 30
    assert recipe.pk is not None


@pytest.mark.django_db
def test_recipe_creation_with_user():
    """Test crearea rețetei cu user + relație inversă"""
    user = User.objects.create_user(username="test1", password="testpass123")

    recipe1 = Recipe.objects.create(
        title="Test reteta 1",
        content="Test content here 1",
        author="Author Test",
        ingredients="Ingrediente test 1",
        nr_ingredients=5,
        time_minutes=25,
        user=user,
    )

    recipe2 = Recipe.objects.create(
        title="Test recipe 2",
        content="Test content here 2",
        author="Author Test2",
        ingredients="Ingrediente test 2",
        nr_ingredients=6,
        time_minutes=40,
        user=user,
    )

    assert recipe1.title == "Test reteta 1"
    assert recipe1.user.username == "test1"
    assert recipe2.user.username == "test1"
    assert user.recipes.count() == 2


@pytest.mark.django_db
def test_recipe_str_method():
    """Test metoda __str__"""
    recipe = Recipe.objects.create(
        title="Supa de legume",
        content="Test content",
        author="Maria Popescu",
        ingredients="Morcovi, telina, pui",
        nr_ingredients=6,
        time_minutes=45,
    )
    expected_str = "Supa de legume, Test content, by Maria Popescu"
    assert str(recipe) == expected_str


@pytest.mark.django_db
def test_recipe_ordering_by_title():
    """Test ordonare după titlu"""
    Recipe.objects.create(
        title="Zucchini Bread",
        content="x",
        author="A",
        ingredients="x",
        nr_ingredients=3,
        time_minutes=30,
    )
    Recipe.objects.create(
        title="Apple Pie",
        content="x",
        author="B",
        ingredients="x",
        nr_ingredients=4,
        time_minutes=50,
    )
    Recipe.objects.create(
        title="Banana Cake",
        content="x",
        author="C",
        ingredients="x",
        nr_ingredients=5,
        time_minutes=40,
    )

    recipes = list(Recipe.objects.all().order_by('title'))
    titles = [r.title for r in recipes]

    assert titles == ["Apple Pie", "Banana Cake", "Zucchini Bread"]