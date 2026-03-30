"""
Fix typo URLs (space or underscore in 'admin panel').

- GET: redirect to /admin-panel/... so the address bar shows the correct URL.
- POST: rewrite path in place (do not redirect, or the POST body would be lost).
"""
from urllib.parse import unquote

from django.http import HttpResponseRedirect


def _rewrite_admin_panel_path(path: str) -> str | None:
    """Return normalized path if this is a known typo, else None."""
    path = unquote(path or '/')
    if path.startswith('/admin panel'):
        return '/admin-panel' + path[len('/admin panel') :]
    if path.startswith('/admin_panel'):
        return '/admin-panel' + path[len('/admin_panel') :]
    return None


class NormalizeAdminPanelPathMiddleware:
    """Map /admin panel/... and /admin_panel/... → /admin-panel/..."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        new_path = _rewrite_admin_panel_path(request.path_info)
        if new_path is None:
            return self.get_response(request)

        if request.method == 'GET':
            qs = request.META.get('QUERY_STRING', '')
            target = new_path if not qs else f'{new_path}?{qs}'
            return HttpResponseRedirect(target)

        request.META['PATH_INFO'] = new_path
        request.path_info = new_path
        script_name = request.META.get('SCRIPT_NAME', '') or ''
        request.path = '%s/%s' % (script_name.rstrip('/'), new_path.replace('/', '', 1))
        return self.get_response(request)
