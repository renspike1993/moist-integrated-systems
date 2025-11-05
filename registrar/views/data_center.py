from django.core.paginator import Paginator
from django.shortcuts import render, redirect,HttpResponse
from ..forms import FolderForm
from ..models import Folder


def get_dashboard(request):
    # Get all folders from the 'registrar' DB
    folders = Folder.objects.all().order_by('-id')

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
            return redirect('registrar:dashboard')
    else:
        form = FolderForm()

    return render(request, 'data-center/add_folder.html', {'form': form})

def edit_folder(request, folder_id):
    # TODO: implement folder edit logic
    return HttpResponse(f"Edit folder {folder_id}")

def delete_folder(request, folder_id):

    # TODO: implement folder delete logic
    return HttpResponse(f"Delete folder {folder_id}")
