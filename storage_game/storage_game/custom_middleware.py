from django.utils.deprecation import MiddlewareMixin

class CustomPortMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Замените '8000' на порт, который вы хотите использовать
        request.META['SERVER_PORT'] = '8000'
