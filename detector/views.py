from django.shortcuts import render
from django.http import FileResponse, JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
import psutil
import joblib
from .models import Visitor
from rest_framework import status
from .models import DetectionLog
from .serializers import DetectionLogSerializer
from django.http import HttpResponse
import subprocess
import platform
import psutil

def get_system_info():
    return {
        'os': platform.system(),
        'os_version': platform.version(),
        'architecture': platform.machine(),
        'cpu': platform.processor(),
        'memory': psutil.virtual_memory().total,
        'disks': [d.device for d in psutil.disk_partitions()],
        'users': psutil.users(),
        'network': psutil.net_if_addrs(),
        'python_version': platform.python_version()
    }

system_info = get_system_info()



@api_view(['POST'])
def scan_keyloggers(request):
    try:
        detected_files = []
        detected_processes = []
        
        # File detection with error handling
        suspicious_files = ["log.txt", "keylogger.py"]
        for file in suspicious_files:
            try:
                if os.path.exists(file):
                    os.remove(file)
                    detected_files.append(file)
            except Exception as file_error:
                print(f"File error: {file_error}")
                continue
                
        # Process detection with error handling
        suspicious_processes = ["keylogger.exe", "spyware.exe"]
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] in suspicious_processes:
                    proc.terminate()
                    detected_processes.append(proc.info['name'])
            except (psutil.NoSuchProcess, psutil.AccessDenied, KeyError) as proc_error:
                print(f"Process error: {proc_error}")
                continue

        return Response({
            "status": "success",
            "files_detected": detected_files,
            "processes_detected": detected_processes
        })
        
    except Exception as e:
        return Response({
            "status": "error",
            "message": f"Scan failed: {str(e)}"
        }, status=500)

def home(request):
    return render(request, 'home.html')

def detection(request):
    return render(request, 'detection.html')

def privacy(request):
    return render(request, 'privacy.html')

def download(request):
    return render(request, 'download.html')
def about_us(request):
    return render(request, 'about_us.html')


@api_view(['GET'])
def visitor_stats(request):
    total_visitors = Visitor.objects.count()
    return Response({"total_visitors": total_visitors})
@api_view(['GET'])
def impression_stats(request):
    total_visitors = Visitor.objects.count()
    return_visitors = Visitor.objects.filter(is_new=False).count()
    impression_rate = (return_visitors / total_visitors * 100) if total_visitors > 0 else 0
    
    return Response({
        'total_visitors': total_visitors,
        'impression_rate': round(impression_rate, 1)
    })
def test_view(request):
    return HttpResponse("WORKING!")

@api_view(['GET'])
def get_detections(request):
    logs = DetectionLog.objects.all().order_by('-timestamp')[:50]  # Get last 50 entries
    serializer = DetectionLogSerializer(logs, many=True)
    return Response(serializer.data)

def download_file(request):
    file_path = os.path.join(settings.BASE_DIR, 'SecureGuard.exe')
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), filename='SecureGuard.exe')
    return JsonResponse({"error": "File not found"}, status=404)

@api_view(['POST'])
def receive_detection(request):
    serializer = DetectionLogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDate


from django.db.models import Count

# Add these imports at the top
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
# Get recent visits

# views.py
@api_view(['POST'])
@csrf_exempt  # For testing only
def track_visit(request):
    try:
        # Create a new visitor entry
        Visitor.objects.create(
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            path=request.META.get('PATH_INFO', '/')
        )
        return Response({"status": "success"})
    except Exception as e:
        return Response({"error": str(e)}, status=500)
# views.py
@api_view(['GET'])
def recent_visits(request):
    try:
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
        
        # Use 'timestamp' instead of 'visit_date'
        visits = (
            Visitor.objects
            .filter(timestamp__gte=start_date)  # Changed here
            .annotate(date=TruncDate('timestamp'))  # Changed here
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )

        # Create date range
        date_dict = {
            (end_date - timedelta(days=x)).date().isoformat(): 0 
            for x in range(30)
        }

        # Populate data
        for visit in visits:
            date_str = visit['date'].isoformat()
            date_dict[date_str] = visit['count']

        dates = sorted(date_dict.keys(), reverse=True)
        counts = [date_dict[date] for date in dates]

        return Response({"dates": dates, "counts": counts})
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)