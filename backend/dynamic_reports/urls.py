from django.urls import path
from .views import (
    text_report_views,
    voice_report_views,
)

urlpatterns = [
    # CU6 - Reportes por texto
    path('text-report/', text_report_views.generate_text_report, name='text-report'),
    path('report-history/', text_report_views.get_report_history, name='report-history'),
    
    # CU7 - Reportes por voz
    path('voice-report/', voice_report_views.process_voice_command, name='voice-report'),
    
    # CU8 y CU9 están integrados en las vistas anteriores
]