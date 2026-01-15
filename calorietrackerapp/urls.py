from django.urls import path
from . import views

app_name = 'calorie_tracker'

urlpatterns = [
    path('home/', views.index, name='index'),
    path('add/', views.add_food, name='add_food'),
    path('edit/<int:food_id>/', views.edit_food, name='edit_food'),
    path('delete/<int:food_id>/', views.delete_food, name='delete_food')
]