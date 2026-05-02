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
    ingredients = models.TextField(max_length=20000)
    nr_ingredients = models.IntegerField(default=0)
    time_minutes = models.IntegerField(default=0)
    servings = models.PositiveIntegerField(null=True, blank=True, verbose_name="Numar portii")

    image = models.ImageField(
        upload_to="recipe_images/",
        null=True,
        blank=True,
        # verbose_name="Imagine"
    )

    # one-to-many relationship here:
    user = models.ForeignKey(
        CustomUser,
        related_name="recipes",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        # verbose_name="Utilizator"
    )
    # # Campuri recomandate pentru sortare și tracking
    # created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creat la")
    # updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizat la")
    #
    # class Meta:
    #     ordering = ['-created_at']  # Cel mai nou primul (recomandat)
    #     # ordering = ['title']              # Alternativ: alfabetic
    #     verbose_name = "Reteta"
    #     verbose_name_plural = "Retete"
    #
    def __str__(self):
        return f"{self.title}, {self.content}, by {self.author}"
