from django.urls import path
from . import views
from .views import track_visit, recent_visits

urlpatterns = [
    path('', views.home, name='home'),
    path('detection/', views.detection, name='detection'),
    path('privacy/', views.privacy, name='privacy'),
    path('about_us/', views.about_us, name='about_us'),

    path('download/', views.download, name='download'),
    path('download-file/', views.download_file, name='download_file'),
    path('api/receive-detection/', views.receive_detection, name='receive_detection'),
    path('test/', views.test_view),
    path('api/track-visit/', track_visit),
    path('api/recent-visits/', recent_visits),
    path('api/visitor-stats/', views.visitor_stats),
    path('api/scan-keyloggers/', views.scan_keyloggers),
    path('api/get-detections/', views.get_detections, name='get_detections'),
]
