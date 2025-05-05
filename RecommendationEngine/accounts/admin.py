from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Developer, Game, News

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Developer)
admin.site.register(Game)
admin.site.register(News)
