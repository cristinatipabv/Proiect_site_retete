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
                  "servings",
                  "image"]
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 12,
                'placeholder': 'Scrie aici pașii de preparare...',
                'style': 'width: 100%; font-family: monospace;'
            }),
            'ingredients': forms.Textarea(attrs={
                'rows': 12,
                'placeholder': 'Scrie ingredientele (unul pe linie)...',
                'style': 'width: 100%; font-family: monospace;'
            }),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'servings': forms.NumberInput(attrs={'min': 1, 'placeholder': 'Ex: 8'}),
        }
        # fields = "__all__"



