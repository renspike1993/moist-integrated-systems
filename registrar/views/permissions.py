# views.py
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib  import messages
from ..models import ExtendedPermission,Permission

def permission_list(request):
    permission_list = Permission.objects.all()
    print(permission_list)
    # permissions = ExtendedPermission.objects.select_related('permission').all()
    return render(request, 'permissions/list.html', {'permissions': permission_list})

def save_permission_button(request, perm_id):
    perm = get_object_or_404(Permission, id=perm_id)

    if request.method == "POST":
        perm.button_class = request.POST.get("button_class")
        perm.button_label = request.POST.get("button_label")
        perm.save()

        messages.success(request, f"Button updated for: {perm.name}")

    # redirect back to whatever page lists permissions
    return redirect("registrar:permission_list")