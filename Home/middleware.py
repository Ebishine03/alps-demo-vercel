from django.shortcuts import redirect
from django.urls import reverse

class RoleBasedRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Check if the user is staff (admin) or employee
            if request.user.is_staff:
                # Admin should be redirected to the admin dashboard
                if request.path == reverse('home'):  # Assuming 'home' is the homepage
                    return redirect('/admin/')  # Update with your admin dashboard URL name
            elif request.user.groups.filter(name='employee').exists():
                # Employee should be redirected to employee dashboard
                if request.path == reverse('home'):  # Assuming 'home' is the homepage
                    return redirect('employee_dashboard')  # Update with your employee dashboard URL name
        return self.get_response(request)
