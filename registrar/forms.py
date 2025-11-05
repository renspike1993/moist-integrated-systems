from django import forms
from .models import Folder

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['folder_name', 'floor_number', 'max_size']
        widgets = {
            'folder_name': forms.TextInput(attrs={'class': 'form-control'}),
            'floor_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_size': forms.NumberInput(attrs={'class': 'form-control'}),
        }
