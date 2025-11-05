from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from ..models import Book


@permission_required('library.view_book')
def get_books(request):
    books = Book.objects.all()
    return render(request, 'book/list.html', {'books': books})
