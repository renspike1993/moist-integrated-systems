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


        if user.has_perm('registrar.view_folder'):
            return reverse_lazy('registrar:dashboard')

        if user.has_perm('library.view_book'):
            return reverse_lazy('library:dashboard')



        return reverse_lazy('accounts:login')


    
    def get_request_details(self):
        meta = self.request.META

        # Proxy chain (if any)
        forwarded_for = meta.get('HTTP_X_FORWARDED_FOR')
        proxy_chain = forwarded_for.split(',') if forwarded_for else []

        # Origin of the request
        origin = meta.get('HTTP_ORIGIN')

        # Previous page (referrer)
        previous_page = meta.get('HTTP_REFERER')

        # Real client IP
        client_ip = proxy_chain[0].strip() if proxy_chain else meta.get('REMOTE_ADDR')
        print({  "client_ip": client_ip,
            "proxy_chain": proxy_chain,
            "origin": origin,
            "previous_page": previous_page,})
        return {
            "client_ip": client_ip,
            "proxy_chain": proxy_chain,
            "origin": origin,
            "previous_page": previous_page,
        }
class WarningLoginView(LoginView):


    def get_failed_url(self):
        user = self.request.user


        if user.has_perm('registrar.view_folder'):
            return reverse_lazy('registrar:dashboard')

        if user.has_perm('library.view_book'):
            return reverse_lazy('library:dashboard')



        return reverse_lazy('accounts:login')
    

    
    def get_request_details(self):
        meta = self.request.META

        # Proxy chain (if any)
        forwarded_for = meta.get('HTTP_X_FORWARDED_FOR')
        proxy_chain = forwarded_for.split(',') if forwarded_for else []

        # Origin of the request
        origin = meta.get('HTTP_ORIGIN')

        # Previous page (referrer)
        previous_page = meta.get('HTTP_REFERER')

        # Real client IP
        client_ip = proxy_chain[0].strip() if proxy_chain else meta.get('REMOTE_ADDR')

        return {
            "client_ip": client_ip,
            "proxy_chain": proxy_chain,
            "origin": origin,
            "previous_page": previous_page,
        }


class CheckClientHttpRequest(LoginView):

    def get_request_details(self):
        meta = self.request.META

        # Proxy chain (if any)
        forwarded_for = meta.get('HTTP_X_FORWARDED_FOR')
        proxy_chain = forwarded_for.split(',') if forwarded_for else []

        # Origin of the request
        origin = meta.get('HTTP_ORIGIN')

        # Previous page (referrer)
        previous_page = meta.get('HTTP_REFERER')

        # Real client IP
        client_ip = proxy_chain[0].strip() if proxy_chain else meta.get('REMOTE_ADDR')

        return {
            "client_ip": client_ip,
            "proxy_chain": proxy_chain,
            "origin": origin,
            "previous_page": previous_page,
        }
