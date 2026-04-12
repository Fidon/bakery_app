from django.shortcuts import redirect
from django.urls import reverse


class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only applies to authenticated users
        if request.user.is_authenticated and request.user.must_change_password:
            allowed_urls = [
                reverse('accounts:set_new_password'),
                reverse('accounts:logout'),
            ]
            if request.path not in allowed_urls:
                return redirect('accounts:set_new_password')

        return self.get_response(request)
    

class NoCacheMiddleware:
    """Prevent browser from caching any page — stops back-button access after logout."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response


class AjaxSessionExpiredMiddleware:
    """
    When an unauthenticated request comes in via Ajax (e.g. session expired),
    return a 401 JSON response instead of redirecting to login.
    Django's default redirect causes the Ajax call to silently receive the
    login page HTML, which breaks all JS error handling.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # If Django is about to redirect an Ajax request to login,
        # intercept and return JSON 401 instead
        if (
            response.status_code == 302
            and request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            and '/login/' in response.get('Location', '')
        ):
            from django.http import JsonResponse
            return JsonResponse(
                {'success': False, 'session_expired': True, 'error': 'Your session has expired. Please sign in again.'},
                status=401
            )

        return response
