from django import forms
from .models import Folder,Student,Program,Curriculum

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
        fields = ['folder', 'curriculum', 'last_name', 'first_name', 'middle_name']
        widgets = {
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'middle_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Middle Name'
            }),
            'folder': forms.Select(attrs={
                'class': 'form-control select2',  # add select2 class here
            }),
            'curriculum': forms.Select(attrs={
                'class': 'form-control',
            }),
        }



class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['program_name']
        widgets = {
            'program_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Program Name'
            }),
        }

class CurriculumForm(forms.ModelForm):
    class Meta:
        model = Curriculum
        fields = ['program', 'major']  # Remove effective_year
        widgets = {
            'program': forms.Select(attrs={'class': 'form-control'}),
            'major': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Major (optional)'}),
        }

class PromotionalReportImportForm(forms.Form):
    file = forms.FileField(
        label="Select CSV file",
        help_text="CSV file with columns: year, semester, first_name, last_name, sub_code, sub_desc, grade, units"
    )
        