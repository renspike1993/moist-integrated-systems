from django.urls import path
from .views import data_center
from .views import student  # import the student views

app_name = "registrar"

urlpatterns = [
    # Folder routes
    path('', data_center.get_dashboard, name='dashboard'),
    path('data-center/add/', data_center.add_folder, name='add_folder'),
    path('data-center/edit/<int:folder_id>/', data_center.edit_folder, name='edit_folder'),
    path('data-center/delete/<int:folder_id>/', data_center.delete_folder, name='delete_folder'),
    path('data-center/import', data_center.import_folders_from_csv, name='import'),

    # Student routes
    path('students/', student.student_list, name='student_list'),
    path('students/add/', student.add_student, name='add_student'),
    path('students/edit/<int:student_id>/', student.edit_student, name='edit_student'),
    path('students/delete/<int:student_id>/', student.delete_student, name='delete_student'),
]
