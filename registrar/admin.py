from django.contrib import admin
from .models import Folder
from django.contrib.auth.models import Permission,User

admin.site.site_url = '/registrar/'  # change this to the URL you want
admin.site.index_title = "Dashboard" 

admin.site.register(Permission)

@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('id', 'folder_name', 'floor_number', 'max_size')
    search_fields = ('folder_name',)
    ordering = ('id',)
