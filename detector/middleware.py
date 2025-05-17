from .models import Visitor
from django.utils import timezone
from datetime import timedelta

class VisitorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:  
            if request.path == '/':
                ip = request.META.get('REMOTE_ADDR')
                user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
            
            # Check for existing visits in last 30 minutes
                recent_visit = Visitor.objects.filter(
                    ip_address=ip,
                    timestamp__gte=timezone.now() - timedelta(minutes=30)
                ).exists()

                if not recent_visit:
                    Visitor.objects.create(
                        ip_address=ip,
                        user_agent=user_agent,
                        path=request.path,
                        is_new=not Visitor.objects.filter(ip_address=ip).exists()
                    )
        except Exception as e:
            print(f"Middleware error: {e}")  # Debug output
        return self.get_response(request)
        