from django.contrib import admin
from app.models import File, User


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['owner', 'file', 'created_at', 'updated_at']
    search_fields = ['owner']
    # prepopulated_fields = {'slug': ('name',)}


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
    search_fields = ['email']
