from django.db import models
from accounts.models import CustomUser

# comenzi de migrare cand se fac orice schimbari intr-un model
# python manage.py makemigrations
# python manage.py migrate
# Create your models here.

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=200, default="No Author")
    ingredients = models.TextField(max_length=200)
    nr_ingredients = models.IntegerField(default=0)
    time_minutes = models.IntegerField(default=0)

    image = models.ImageField(
        upload_to="recipe_images/",
        null=True,
        blank=True,
    )

    # one-to-many relationship here:
    user = models.ForeignKey(
        CustomUser,
        related_name="recipes",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    # related_name="recipes" -> parametru adaugat automat fiecarui obiect CustomUser, unde avem acces la o lista cu cartile care apartin user-ului.

    def __str__(self):
        return f"{self.title}, {self.content}, by {self.author}"
