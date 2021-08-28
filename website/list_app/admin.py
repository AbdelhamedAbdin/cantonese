from django.contrib import admin
from .models import Words, Characters, Actors, Films, Sentences, Tokens


@admin.register(Films)
class CustomFilmAdmin(admin.ModelAdmin):
    list_display = ['id', 'genre', 'hkmdb_id', 'name_en', 'name_zh', 'visible', 'year']


@admin.register(Sentences)
class CustomSentenceAdmin(admin.ModelAdmin):
    list_display = ['id', 'actor_id', 'film_id', 'orth', 'pron', 'tag', 'slug_c']


@admin.register(Tokens)
class CustomTokenAdmin(admin.ModelAdmin):
    list_display = ['id', 'word_id', 'sentence_id', 'position']


@admin.register(Words)
class CustomWordAdmin(admin.ModelAdmin):
    list_display = ['id', 'orth', 'tag', 'pron', 'freq']


@admin.register(Characters)
class CustomCharacterAdmin(admin.ModelAdmin):
    list_display = ['id', 'freq', 'character']


@admin.register(Actors)
class CustomActorAdmin(admin.ModelAdmin):
    list_display = ['id', 'age', 'code', 'gender', 'name_en', 'name_zh']
