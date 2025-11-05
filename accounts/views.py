from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def form_invalid(self, form):
        # Called when login fails
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)

    def get_success_url(self):
        user = self.request.user

        if user.has_perm('library.view_book'):
            return reverse_lazy('library:dashboard')

        if user.has_perm('registrar.view_folder'):
            return reverse_lazy('registrar:dashboard')

        return reverse_lazy('accounts:login')
