from django.contrib import admin
from .models import Folder

@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('id', 'folder_name', 'floor_number', 'max_size')
    search_fields = ('folder_name',)
