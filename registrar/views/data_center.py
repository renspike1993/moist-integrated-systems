import csv
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from django.db import transaction
from ..forms import FolderForm
from ..models import Folder, Student
from django.contrib.auth.decorators import login_required, permission_required

# --- Dashboard ---
@login_required
@permission_required('registrar.view_folder', login_url='accounts:login')
def get_dashboard(request):
    query = request.GET.get('q', '')

    if query:
        folders = Folder.objects.filter(folder_name__icontains=query).order_by('id')
    else:
        folders = Folder.objects.all().order_by('id')

    paginator = Paginator(folders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'data-center/folders.html', context)


# --- Add folder ---
@login_required
@permission_required('registrar.add_folder', login_url='accounts:login')
def add_folder(request):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.save()
            messages.success(request, "Folder added successfully!")
            return redirect('registrar:dashboard')
    else:
        form = FolderForm()

    return render(request, 'data-center/add_folder.html', {'form': form})


# --- Edit folder ---
@login_required
@permission_required('registrar.change_folder', login_url='accounts:login')
def edit_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)

    if request.method == 'POST':
        form = FolderForm(request.POST, instance=folder)
        if form.is_valid():
            form.save()
            messages.success(request, "Folder Edited successfully!")
            return redirect('registrar:dashboard')
    else:
        form = FolderForm(instance=folder)

    return render(request, 'data-center/edit_folder.html', {'form': form, 'folder': folder})


# --- Delete folder ---
@login_required
@permission_required('registrar.delete_folder', login_url='accounts:login')
def delete_folder(request, folder_id):
    folder = get_object_or_404(Folder, pk=folder_id)
    if request.method == 'POST':
        folder.delete()
        messages.success(request, "Folder deleted successfully!")
        return redirect('registrar:dashboard')
    return render(request, 'data-center/delete_folder.html', {'folder': folder})


# --- Import CSV ---
@login_required
@permission_required('registrar.add_folder', login_url='accounts:login')
def import_folders_from_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']

        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            with transaction.atomic():
                for row in reader:
                    folder_name = row.get('folder_name', '').strip()
                    if not folder_name:
                        continue

                    folder, created = Folder.objects.get_or_create(
                        folder_name=folder_name,
                        defaults={'floor_number': 0, 'max_size': 0}
                    )

                    if row.get('lname') and row.get('fname'):
                        Student.objects.create(
                            last_name=row.get('lname').strip(),
                            first_name=row.get('fname').strip(),
                            middle_name=row.get('midname', '').strip(),
                            folder=folder
                        )

            messages.success(request, "CSV processed successfully!")
        except Exception as e:
            messages.error(request, f"Error processing CSV: {str(e)}")

        return redirect('registrar:dashboard')

    return render(request, 'data-center/import_folders.html')
