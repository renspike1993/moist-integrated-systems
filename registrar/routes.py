from django.urls import path
from . import views

app_name = "registrar"

urlpatterns = [
    path('', views.get_dashboard, name='dashboard'),
    path('programs/', views.get_program, name='programs'),


]
