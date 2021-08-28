from django.urls import path, re_path
from . import views

app_name = "list_app"

urlpatterns = [
    path('words/', views.listWords, name="words"),
    path('characters/', views.listCharacters, name="characters"),
    path('actors/', views.listActors, name="actors"),
    path('films/', views.listFilms, name="films")
]
