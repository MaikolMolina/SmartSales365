# backend/dynamic_reports/views/voice_report_views.py
import os
import traceback
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import speech_recognition as sr

# Importamos el conversor (usa pydub internamente)
from ..utils.audio_converter import convertir_audio_a_wav, ensure_ffmpeg_configured

# Configuramos ffmpeg/ffprobe para todo el proceso
try:
    ffmpeg_path, ffprobe_path = ensure_ffmpeg_configured()
    print("VOICE VIEW - ffmpeg:", ffmpeg_path, "exists?", os.path.exists(ffmpeg_path))
    print("VOICE VIEW - ffprobe:", ffprobe_path, "exists?", os.path.exists(ffprobe_path))
except Exception as e:
    print("VOICE VIEW - ERROR configurando ffmpeg/ffprobe:", str(e))
    ffmpeg_path = ffprobe_path = None


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_voice_command(request):
    """
    CU7 - Procesar comando de voz y generar reporte.
    Requiere que ffmpeg/ffprobe estén disponibles (configurados por audio_converter.ensure_ffmpeg_configured).
    """
    try:
        # Validar configuración de ffmpeg
        if ffmpeg_path is None or ffprobe_path is None:
            return Response(
                {'error': 'FFmpeg/ffprobe no están configurados en el servidor. Revisa los logs.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Validar audio
        audio_file = request.FILES.get('audio')
        if not audio_file:
            return Response({'error': 'Archivo de audio requerido'}, status=status.HTTP_400_BAD_REQUEST)

        # Convertir el audio a WAV
        converted_audio_path = convertir_audio_a_wav(audio_file)

        try:
            # Transcribir a texto con SpeechRecognition
            recognizer = sr.Recognizer()
            with sr.AudioFile(converted_audio_path) as source:
                audio_data = recognizer.record(source)

            text = recognizer.recognize_google(audio_data, language='es-ES')

            # Determinar formato de salida (por defecto JSON)
            formato = request.data.get('formato', 'JSON')

            # Importar y llamar directamente al generador de reportes
            from .text_report_views import generate_text_report

            # ✅ Llamamos directamente pasando los parámetros necesarios
            response = generate_text_report(
                prompt=text,
                formato=formato,
                user=request.user
            )

            return Response(response, status=status.HTTP_200_OK)

        finally:
            # Borramos el archivo temporal
            if converted_audio_path and os.path.exists(converted_audio_path):
                try:
                    os.unlink(converted_audio_path)
                except Exception:
                    pass

    except sr.UnknownValueError:
        return Response({'error': 'No se pudo entender el audio.'},
                        status=status.HTTP_400_BAD_REQUEST)
    except sr.RequestError as e:
        return Response({'error': f'Error en el servicio de reconocimiento: {str(e)}'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        traceback.print_exc()
        return Response({'error': f'Error procesando comando de voz: {str(e)}'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
