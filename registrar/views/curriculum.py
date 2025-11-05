import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from ..models import Curriculum, Program, Course
from ..forms import CurriculumForm

# --- List Curriculums ---
@login_required
@permission_required('registrar.view_curriculum', login_url='accounts:login')
def curriculum_list(request):
    query = request.GET.get('q', '')
    
    if query:
        curriculums = Curriculum.objects.filter(
            program__program_name__icontains=query
        ).order_by('program__program_name', 'major')
    else:
        curriculums = Curriculum.objects.all().order_by('program__program_name', 'major')
    
    paginator = Paginator(curriculums, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'curriculum/curriculum_list.html', {
        'page_obj': page_obj,
        'query': query
    })

# --- Add Curriculum ---
@login_required
@permission_required('registrar.add_curriculum', login_url='accounts:login')
def add_curriculum(request):
    if request.method == 'POST':
        form = CurriculumForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Curriculum added successfully!")
            return redirect('registrar:curriculum_list')
    else:
        form = CurriculumForm()
    return render(request, 'curriculum/add_curriculum.html', {'form': form})


# --- Edit Curriculum ---
@login_required
@permission_required('registrar.change_curriculum', login_url='accounts:login')
def edit_curriculum(request, curriculum_id):
    curriculum = get_object_or_404(Curriculum, id=curriculum_id)

    # Get all courses for this curriculum
    courses = Course.objects.filter(curriculum=curriculum).order_by('year_level', 'semester_offered', 'course_code')

    if request.method == 'POST':
        form = CurriculumForm(request.POST, instance=curriculum)
        if form.is_valid():
            form.save()
            messages.success(request, "Curriculum updated successfully!")
            return redirect('registrar:curriculum_list')
    else:
        form = CurriculumForm(instance=curriculum)

    context = {
        'form': form,
        'curriculum': curriculum,
        'courses': courses,  # pass courses to the template
    }
    return render(request, 'curriculum/edit_curriculum.html', context)


# --- Delete Curriculum ---
@login_required
@permission_required('registrar.delete_curriculum', login_url='accounts:login')
def delete_curriculum(request, curriculum_id):
    curriculum = get_object_or_404(Curriculum, id=curriculum_id)
    if request.method == 'POST':
        curriculum.delete()
        messages.success(request, "Curriculum deleted successfully!")
        return redirect('registrar:curriculum_list')
    return render(request, 'curriculum/delete_curriculum.html', {'curriculum': curriculum})

# --- Import Curriculum from CSV ---
@login_required
@permission_required('registrar.add_course', login_url='accounts:login')
def import_curriculum_from_csv(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]
        data = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(data)

        total = 0
        saved = 0
        skipped = []

        for row in reader:
            total += 1
            try:
                program_name = row.get("program", "").strip()
                major = row.get("major", "").strip()
                curriculum_name = row.get("curriculum_name", "").strip()  # Optional
                year = row.get("year", "").strip()
                semester = row.get("semester", "").strip()
                course_code = row.get("course_code", "").strip()
                course_description = row.get("course_description", "").strip()
                lec_unit = int(row.get("lec_unit", 0))
                lab_unit = int(row.get("lab_unit", 0))
                prerequisite = row.get("prerequisite", "").strip()

                # Skip incomplete rows
                if not (program_name and course_code):
                    skipped.append((total, "Missing required data"))
                    continue

                # Get or create Program
                program, _ = Program.objects.get_or_create(program_name=program_name)

                # Get or create Curriculum
                curriculum, _ = Curriculum.objects.get_or_create(
                    program=program,
                    major=major or None
                )

                # Create Course
                Course.objects.create(
                    curriculum=curriculum,
                    course_code=course_code,
                    course_title=course_description or "No Title",
                    lec_units=lec_unit,
                    lab_units=lab_unit,
                    prerequisites=prerequisite,
                    semester_offered=semester or "Not Specified",
                    year_level=int(year) if year.isdigit() else 0
                )
                saved += 1

            except Exception as e:
                skipped.append((total, str(e)))

        messages.success(
            request,
            f"Import complete: {saved} courses saved, {len(skipped)} skipped out of {total} rows."
        )

        if skipped:
            with open("skipped_curriculum.log", "w", encoding="utf-8") as log_file:
                for line, reason in skipped:
                    log_file.write(f"Line {line}: {reason}\n")

        return redirect("registrar:dashboard")

    return render(request, "curriculum/import_curriculum.html", {
        'instructions': "CSV columns: program, major, curriculum_name, year, semester, course_code, course_description, lec_unit, lab_unit, prerequisite"
    })
