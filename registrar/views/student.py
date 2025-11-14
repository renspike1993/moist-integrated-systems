from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from ..models import Student
from ..forms import StudentForm
from django.core.paginator import Paginator
from django.db.models import Q

import csv
from django.db import transaction
from ..models import Folder, Student


# ----------------------
# List students
# ----------------------
@login_required
@permission_required('registrar.view_student', login_url='accounts:login')
def student_list(request):
    query = request.GET.get('q', '').strip()
    
    # Base queryset with folder prefetch to reduce queries
    students_qs = Student.objects.select_related('folder').all().order_by('last_name', 'first_name')

    # If there's a search query
    if query:
        terms = query.split()  # split by space
        q_objects = Q()  # empty Q object
        for term in terms:
            q_objects &= (Q(last_name__icontains=term) |
                          Q(first_name__icontains=term) |
                          Q(middle_name__icontains=term) |
                          Q(folder__folder_name__icontains=term))
        students_qs = students_qs.filter(q_objects)

    # Pagination
    paginator = Paginator(students_qs, 10)  # 10 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
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

import csv


@login_required
@permission_required('registrar.add_student', raise_exception=True)

@login_required
@permission_required('registrar.add_student', login_url='accounts:login')
def import_students_from_csv(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]

        try:
            data = csv_file.read().decode("utf-8").splitlines()
        except UnicodeDecodeError:
            messages.error(request, "Error reading CSV file. Please ensure it is UTF-8 encoded.")
            return redirect("registrar:student_list")

        reader = csv.DictReader(data)

        total = 0
        saved = 0
        failed = 0
        errors = []

        for row in reader:
            total += 1
            folder_name = row.get("folder_name", "").strip()
            last_name = row.get("last_name", "").strip()
            first_name = row.get("first_name", "").strip()
            middle_name = row.get("middle_name", "").strip()

            # Validate required fields
            if not folder_name or not last_name or not first_name:
                failed += 1
                errors.append(f"Row {total}: Missing required data")
                continue

            # Get or create folder
            folder, _ = Folder.objects.get_or_create(folder_name=folder_name)

            # Create student (duplicates allowed)
            try:
                Student.objects.create(
                    folder=folder,
                    last_name=last_name,
                    first_name=first_name,
                    middle_name=middle_name
                )
                saved += 1
            except Exception as e:
                failed += 1
                errors.append(f"Row {total}: {str(e)}")

        # Write skipped or error logs (optional)
        if errors:
            with open("import_errors.log", "w", encoding="utf-8") as log_file:
                for err in errors:
                    log_file.write(err + "\n")

        messages.success(
            request,
            f"Import complete: {saved} students saved out of {total} rows. ({failed} failed)"
        )
        return redirect("registrar:student_list")

    return render(request, "student/import_students.html")
