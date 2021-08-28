from django.contrib import admin
from .models import User, Profile, History

admin.site.register(Profile)


@admin.register(History)
class CustomHistory(admin.ModelAdmin):
    list_display = ['user', 'history', 'verb_option', 'action_option', 'history_time']
    list_filter = ['history', 'verb_option']


@admin.register(User)
class CustomUser(admin.ModelAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'admin']
    readonly_fields = ['password', 'last_login']
