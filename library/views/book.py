from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from ..models import Book


@permission_required('library.view_book')
def get_books(request):
    return render(request, 'book/list.html')


def attendance_in(request):
    return render(request, 'attendance_in.html')

def attendance_out(request):
    return render(request, 'attendance_out.html')


