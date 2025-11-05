from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required, permission_required
from ..forms import ProgramForm
from ..models import Program
import csv

# --- Program List (Dashboard) -
@login_required
@permission_required('registrar.view_program', login_url='accounts:login')
def get_programs(request):
    query = request.GET.get('q', '')

    if query:
        programs = Program.objects.filter(program_name__icontains=query).order_by('id')
    else:
        programs = Program.objects.all().order_by('id')

    paginator = Paginator(programs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'programs/program_list.html', context)


# --- Add Program ---
@login_required
@permission_required('registrar.add_program', login_url='accounts:login')
def add_program(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Program added successfully!")
            return redirect('registrar:programs')
    else:
        form = ProgramForm()

    return render(request, 'programs/add_program.html', {'form': form})


# --- Edit Program ---
@login_required
@permission_required('registrar.change_program', login_url='accounts:login')
def edit_program(request, program_id):
    program = get_object_or_404(Program, id=program_id)

    if request.method == 'POST':
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            messages.success(request, "Program updated successfully!")
            return redirect('registrar:programs')
    else:
        form = ProgramForm(instance=program)

    return render(request, 'programs/edit_program.html', {'form': form, 'program': program})


# --- Delete Program ---
@login_required
@permission_required('registrar.delete_program', login_url='accounts:login')
def delete_program(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    if request.method == 'POST':
        program.delete()
        messages.success(request, "Program deleted successfully!")
        return redirect('registrar:programs')
    return render(request, 'programs/delete_program.html', {'program': program})


# --- Import Programs from CSV ---
@login_required
@permission_required('registrar.add_program', login_url='accounts:login')
def import_programs_from_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']

        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            with transaction.atomic():
                for row in reader:
                    program_name = row.get('program', '').strip()
                    if not program_name:
                        continue
                    Program.objects.get_or_create(program_name=program_name)

            messages.success(request, "Programs imported successfully!")
        except Exception as e:
            messages.error(request, f"Error processing CSV: {str(e)}")

        return redirect('registrar:programs')

    return render(request, 'programs/import_programs.html')
