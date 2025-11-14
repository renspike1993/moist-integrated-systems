from django.urls import path
from .views import data_center,student,curriculum,program, promotional_report, system_integ

app_name = "registrar"

urlpatterns = [



    # Folder routes
    path('', data_center.get_dashboard, name='dashboard'),
    path('data-center/add/', data_center.add_folder, name='add_folder'),
    path('data-center/view/<int:folder_id>/', data_center.view_folder, name='view_folder'),
    path('data-center/edit/<int:folder_id>/', data_center.edit_folder, name='edit_folder'),
    path('data-center/delete/<int:folder_id>/', data_center.delete_folder, name='delete_folder'),
    path('data-center/import', data_center.import_folders_from_csv, name='import'),
    path('folder/<int:folder_id>/add-student/', data_center.add_student_to_folder, name='add_student_to_folder'),
    path('remove-student/<int:student_id>/', data_center.remove_student_from_folder, name='remove_student_from_folder'),


    path('system-integrations/', system_integ.system_integrations , name='system_integrations'),


    # Student routes
    path('students/', student.student_list, name='student_list'),
    path('students/add/', student.add_student, name='add_student'),
    path('students/edit/<int:student_id>/', student.edit_student, name='edit_student'),
    path('students/delete/<int:student_id>/', student.delete_student, name='delete_student'),
    path('students/import/', student.import_students_from_csv, name='import_students'),
    # Program routes
    path('programs/', program.get_programs, name='programs'),
    path('programs/add/', program.add_program, name='add_program'),
    path('programs/edit/<int:program_id>/', program.edit_program, name='edit_program'),
    path('programs/delete/<int:program_id>/', program.delete_program, name='delete_program'),
    path('programs/import/', program.import_programs_from_csv, name='import_programs'),


    # Curriculum routes
    path('curriculums/', curriculum.curriculum_list, name='curriculum_list'),
    path('curriculums/add/', curriculum.add_curriculum, name='add_curriculum'),
    path('curriculums/edit/<int:curriculum_id>/', curriculum.edit_curriculum, name='edit_curriculum'),
    path('curriculums/delete/<int:curriculum_id>/', curriculum.delete_curriculum, name='delete_curriculum'),
    path('curriculum/import/', curriculum.import_curriculum_from_csv, name='import_curriculum'),

    path('import-promotional-report/', promotional_report.import_promotional_report, name='import_promotional_report'),
    path('promotional-report-summary/', promotional_report.promotional_report_summary, name='promotional_report_summary'),
    path('promotional/<int:year>/<str:semester>/', promotional_report.promotional_detail, name='promotional_detail'),
]
