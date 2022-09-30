from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        auth_included_path = []

        if request.path_info in auth_included_path:
            if not request.session.get('user_info'):
                return redirect('userauth/login/1/')

        return None

    def respond_request(self, request, responce):
        return responce
