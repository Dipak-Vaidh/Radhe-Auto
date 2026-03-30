"""Project-level views (health checks, etc.)."""
from django.http import HttpResponse


def health(request):
    """Plain-text OK for load balancers / uptime monitors. No DB hit."""
    return HttpResponse('ok', content_type='text/plain; charset=utf-8')
