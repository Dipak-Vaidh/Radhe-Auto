"""
Custom adapter for django-allauth to handle redirects with next param.
"""
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        """Redirect to ?next= if present, else default."""
        next_url = request.GET.get('next') or request.session.get('next')
        if next_url and next_url.startswith('/'):
            return next_url
        return settings.LOGIN_REDIRECT_URL
