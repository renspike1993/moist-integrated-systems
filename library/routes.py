from django.urls import path
from .views import book
 
app_name = "library"

urlpatterns = [
    # Library dashboard (list of books)
    path('', book.get_books, name='dashboard'),

    path('attendance-log/in', book.attendance_in, name='in'),

    path('attendance-log/out', book.attendance_out, name='out'),



]
