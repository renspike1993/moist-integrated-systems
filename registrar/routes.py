from django.urls import path
from .views import data_center

app_name = "registrar"

urlpatterns = [
    path('', data_center.get_dashboard, name='dashboard'),
    path('data-center/add/', data_center.add_folder, name='add_folder'),
    path('data-center/edit/<int:folder_id>/', data_center.edit_folder, name='edit_folder'),
    path('data-center/delete/<int:folder_id>/', data_center.delete_folder, name='delete_folder'),

]
