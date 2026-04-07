from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title",
                  "content",
                  "ingredients",
                  "nr_ingredients",
                  "time_minutes",
                  "author",
                  "image"]
        # fields = "__all__"
