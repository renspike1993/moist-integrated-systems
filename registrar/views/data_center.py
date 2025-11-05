from django.core.paginator import Paginator
from django.shortcuts import render, redirect,HttpResponse,get_object_or_404
from ..forms import FolderForm
from ..models import Folder
from django.contrib import messages

def get_dashboard(request):
    # Get all folders from the 'registrar' DB
    folders = Folder.objects.all().order_by('id')

    # --- Pagination setup ---
    paginator = Paginator(folders, 10)  # 10 folders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'data-center/folders.html', context)


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

def edit_folder(request, folder_id):
    # Retrieve the folder or return 404 if not found
    folder = get_object_or_404(Folder, id=folder_id)

    if request.method == 'POST':
        # Bind the form to POST data and the existing folder instance
        form = FolderForm(request.POST, instance=folder)
        if form.is_valid():
            # Save changes to the database
            form.save()
            messages.success(request, "Folder Edited successfully!")
            return redirect('registrar:dashboard')
    else:
        # Pre-fill the form with the folder's current data
        form = FolderForm(instance=folder)

    # Render the edit form template
    return render(request, 'data-center/edit_folder.html', {'form': form, 'folder': folder})

def delete_folder(request, folder_id):
    folder = get_object_or_404(Folder, pk=folder_id)
    if request.method == 'POST':
        folder.delete()
        messages.success(request, "Folder deleted successfully!")
        return redirect('registrar:dashboard')
    return render(request, 'data-center/delete_folder.html', {'folder': folder})
