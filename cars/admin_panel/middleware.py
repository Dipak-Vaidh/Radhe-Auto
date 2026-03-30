from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


class StaffAdminPanelMiddleware:
    """
    Restrict /admin-panel/* to authenticated staff.
    Login and logout routes are exempt.
    """

    PREFIX = '/admin-panel'
    EXEMPT = (
        '/admin-panel/login/',
        '/admin-panel/login',
        '/admin-panel/logout/',
        '/admin-panel/logout',
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if path.startswith(self.PREFIX) and path not in self.EXEMPT:
            if not request.user.is_authenticated:
                if path.startswith(self.PREFIX + '/api/'):
                    from django.http import JsonResponse

                    return JsonResponse({'error': 'authentication required'}, status=401)
                login_url = reverse('admin_panel:login')
                return redirect(f'{login_url}?next={request.path}')
            if not request.user.is_staff:
                if path.startswith(self.PREFIX + '/api/'):
                    from django.http import JsonResponse

                    return JsonResponse({'error': 'staff only'}, status=403)
                messages.warning(request, 'Staff access only.')
                return redirect('home')
        return self.get_response(request)
