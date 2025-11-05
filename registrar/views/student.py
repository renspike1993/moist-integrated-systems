from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from ..models import Student
from ..forms import StudentForm
from django.core.paginator import Paginator
from django.db.models import Q


# ----------------------
# List students
# ----------------------
@login_required
@permission_required('registrar.view_student', login_url='accounts:login')
def student_list(request):
    query = request.GET.get('q', '')

    if query:
        students = Student.objects.filter(
            Q(last_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(middle_name__icontains=query) |
            Q(folder__folder_name__icontains=query)
        ).order_by('last_name', 'first_name')
    else:
        students = Student.objects.all().order_by('last_name', 'first_name')

    # Pagination
    paginator = Paginator(students, 10)  # 10 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query
    }
    return render(request, 'student/students.html', context)

# ----------------------
# Add student
# ----------------------
@login_required
@permission_required('registrar.add_student', login_url='accounts:login')
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully!")
            return redirect('registrar:student_list')
    else:
        form = StudentForm()

    return render(request, 'student/add_student.html', {'form': form})


# ----------------------
# Edit student
# ----------------------
@login_required
@permission_required('registrar.change_student', login_url='accounts:login')
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully!")
            return redirect('registrar:student_list')
    else:
        form = StudentForm(instance=student)

    return render(request, 'student/edit_student.html', {'form': form, 'student': student})


# ----------------------
# Delete student
# ----------------------
@login_required
@permission_required('registrar.delete_student', login_url='accounts:login')
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        messages.success(request, "Student deleted successfully!")
        return redirect('registrar:student_list')

    return render(request, 'student/delete_student.html', {'student': student})
