from django.urls import path
from .views import book
 
app_name = "library"

urlpatterns = [
    # Library dashboard (list of books)
    path('', book.get_books, name='dashboard'),
]
