from datetime import datetime, timezone
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication

# Автоматическое использование токенов из куки при запросах
class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = self.get_access_token(request)
        refresh_token = self.get_refresh_token(request)

        if access_token:
            try:
                token = AccessToken(access_token)
                exp = datetime.utcfromtimestamp(token['exp'])
                if exp < datetime.utcnow():
                    raise TokenError("Access token expired")
                self.set_auth_header(request, access_token)
            except TokenError:
                if refresh_token:
                    new_token = self.refresh_access_token(refresh_token)
                    if new_token:
                        self.set_auth_header(request, new_token)
                        request._new_access_token = new_token
                    else:
                        self.flag_clear_cookies(request)
        elif refresh_token:
            new_token = self.refresh_access_token(refresh_token)
            if new_token:
                self.set_auth_header(request, new_token)
                request._new_access_token = new_token
            else:
                self.flag_clear_cookies(request)

    def get_access_token(self, request):
        # Приоритет — заголовок Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            return auth_header.split(' ')[1]
        # Или из куки
        return request.COOKIES.get('access_token')

    def get_refresh_token(self, request):
        return request.COOKIES.get('refresh_token')

    def set_auth_header(self, request, token):
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'

    def refresh_access_token(self, refresh_token):
        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            return new_access_token
        except TokenError:
            return None

    def flag_clear_cookies(self, request):
        request._clear_tokens = True

    def process_response(self, request, response):
        if getattr(request, '_new_access_token', None):
            access_exp = AccessToken(request._new_access_token)['exp']
            response.set_cookie(
                key='access_token',
                value=request._new_access_token,
                httponly=True,
                secure=False,  # Используйте True в продакшене
                samesite='Lax',
                expires=datetime.utcfromtimestamp(access_exp)
            )

        if getattr(request, '_clear_tokens', False):
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')

        return response