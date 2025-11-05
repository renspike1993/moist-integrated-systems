from django.urls import path
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView

app_name = 'accounts'  # important for reverse_lazy('accounts:login')

urlpatterns = [
    # Login
    path('login/', CustomLoginView.as_view(), name='login'),

    # Logout
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
]
