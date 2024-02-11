# middlewares.py
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.middleware import get_user

def get_user_lazy(request):
    user = get_user(request)
    return user if user.is_authenticated else AnonymousUser()

class SetUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request._user = SimpleLazyObject(lambda: get_user_lazy(request))
        response = self.get_response(request)
        return response
