"""Shared HTTP helpers for API views."""


def get_bearer_token(request):
    """Extract the JWT bearer token from the Authorization header."""
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    if auth_header.startswith('Bearer '):
        return auth_header.split(' ', 1)[1]
    return None
