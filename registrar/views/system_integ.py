from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def system_integrations(request):
    integrations = [
        {'name': 'Library (OPAC)', 'url': '/library/'},
        {'name': 'Entrance Exam', 'url': '/accounts/login/'},
        {'name': 'Intramurals', 'url': '/accounts/login/'},
        {'name': 'Student Government Election (CSG)', 'url': '/accounts/login/'},
        {'name': 'Attendance Logs (QR-CODE)', 'url': '/accounts/login/'},
        {'name': 'System Administrator', 'url': '/admin/'},
    ]
    context = {
        'integrations': integrations,
    }
    return render(request, 'integrations/system_integrations.html', context)
