from django.contrib import admin
from .models import Program, Curriculum, Course, Folder, Student

# --- Program ---
@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('id', 'program_name')
    search_fields = ('program_name',)

# --- Curriculum ---
@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ('id', 'program', 'major')
    list_filter = ('program',)
    search_fields = ('program__program_name', 'major')

# --- Course ---
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'course_code', 'course_title', 'curriculum', 'year_level', 'semester_offered')
    list_filter = ('curriculum', 'semester_offered', 'year_level')
    search_fields = ('course_code', 'course_title', 'curriculum__program__program_name')

# --- Folder ---
@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('id', 'folder_name', 'floor_number', 'max_size')
    search_fields = ('folder_name',)

# --- Student ---
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'folder', 'curriculum')
    list_filter = ('folder', 'curriculum')
    search_fields = ('last_name', 'first_name', 'middle_name')
