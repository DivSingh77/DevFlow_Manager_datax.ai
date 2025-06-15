from django.utils.timezone import now
from .models import UserAction, ActionLog

class UserActionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if hasattr(request, 'user') and request.user.is_authenticated:
            if request.method in ['POST', 'PUT', 'DELETE']:
                UserAction.objects.create(
                    user=request.user,
                    action=f"{request.method} {request.path}",
                    ip_address=self.get_client_ip(request),
                    details={
                        'method': request.method,
                        'path': request.path,
                        'data': request.POST.dict()
                    }
                )
        
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


class ActionLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated and request.method in ['POST', 'PUT', 'DELETE']:
            ip = request.META.get('REMOTE_ADDR', '')
            ActionLog.objects.create(
                user=request.user,
                action=f"{request.method} {request.path}",
                ip_address=ip,
                timestamp=now()
            )

        return response
