from django import forms
from .models import Folder,Student

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['folder_name', 'floor_number', 'max_size']
        widgets = {
            'folder_name': forms.TextInput(attrs={'class': 'form-control'}),
            'floor_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_size': forms.NumberInput(attrs={'class': 'form-control'}),
        }

        
class CSVImportForm(forms.Form):
    csv_file = forms.FileField(
        label="Select CSV File",
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['folder', 'last_name', 'first_name', 'middle_name']
        widgets = {
            'folder': forms.Select(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Middle Name'}),
        }