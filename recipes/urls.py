from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list, name="recipe_list"),
    path('recipes/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('create_recipe/', views.create_recipe, name="create_recipe"),
    path('check_recipe_count/', views.check_recipe_count, name="check_recipe_count"),
    path('recipe/<int:pk>/delete/', views.delete_recipe, name="delete_recipe"),
    path('recipe/<int:pk>/update/', views.update_recipe, name="update_recipe"),
    path('recipe/<int:pk>/delete_image/', views.delete_recipe_image, name="delete_recipe_image"),
    path('user/<int:pk>/recipes/', views.user_recipes, name="user_recipes"),
    path('search/', views.search_recipes, name="search_recipes"),
    path('api_simple_endpoint/', views.simple_endpoint, name="simple"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
