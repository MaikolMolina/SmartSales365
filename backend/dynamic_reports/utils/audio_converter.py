import os
import tempfile
from pydub import AudioSegment


def _candidate_ffmpeg_paths():
    """
    Devuelve posibles ubicaciones de ffmpeg y ffprobe.
    Adaptado a tu estructura:
    backend/
        ├── ffmpeg/
        │   └── bin/
        │       ├── ffmpeg.exe
        │       └── ffprobe.exe
        └── dynamic_reports/
            └── utils/
    """
    here = os.path.dirname(os.path.abspath(__file__))            # .../backend/dynamic_reports/utils
    backend_dir = os.path.normpath(os.path.join(here, '..', '..'))  # .../backend
    project_root = os.path.normpath(os.path.join(backend_dir, '..'))  # .../SmartSales365

    candidates = [
        os.path.join(backend_dir, 'ffmpeg', 'bin'),              # ✅ tu caso real
        os.path.join(project_root, 'backend', 'ffmpeg', 'bin'),  # redundante pero seguro
        os.path.join(project_root, 'ffmpeg', 'bin'),             # por si lo mueves en el futuro
    ]

    # eliminar duplicados y normalizar
    paths = []
    for p in candidates:
        pnorm = os.path.normpath(os.path.abspath(p))
        if pnorm not in paths:
            paths.append(pnorm)
    return paths


def find_ffmpeg_bin():
    """Busca ffmpeg.exe y ffprobe.exe en las rutas candidatas."""
    for base in _candidate_ffmpeg_paths():
        ffmpeg = os.path.join(base, 'ffmpeg.exe')
        ffprobe = os.path.join(base, 'ffprobe.exe')
        if os.path.exists(ffmpeg) and os.path.exists(ffprobe):
            return ffmpeg, ffprobe
    return None, None


def ensure_ffmpeg_configured():
    """
    Configura ffmpeg y ffprobe para pydub.
    Retorna (ffmpeg_path, ffprobe_path) o lanza excepción si no se encuentran.
    """
    ffmpeg_path, ffprobe_path = find_ffmpeg_bin()
    if not ffmpeg_path or not ffprobe_path:
        raise Exception("No se encontró ffmpeg/ffprobe en las rutas: " + ", ".join(_candidate_ffmpeg_paths()))

    # Configurar pydub y variables de entorno
    os.environ["FFMPEG_BINARY"] = ffmpeg_path
    os.environ["FFPROBE_BINARY"] = ffprobe_path
    os.environ["PATH"] = os.path.dirname(ffmpeg_path) + os.pathsep + os.environ.get("PATH", "")

    AudioSegment.converter = ffmpeg_path
    AudioSegment.ffprobe = ffprobe_path
    return ffmpeg_path, ffprobe_path


def convertir_audio_a_wav(uploaded_file):
    """
    Convierte un archivo subido (WebM/OGG/MP3...) a WAV (PCM16, mono, 16kHz).
    Devuelve la ruta del archivo WAV temporal.
    """
    ensure_ffmpeg_configured()

    # Guardar temporalmente el archivo recibido
    original_name = getattr(uploaded_file, 'name', 'audio')
    suffix = os.path.splitext(original_name)[1] or '.tmp'
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_in:
        for chunk in uploaded_file.chunks():
            tmp_in.write(chunk)
        tmp_in_path = tmp_in.name

    # Archivo temporal WAV de salida
    tmp_out = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tmp_out_path = tmp_out.name
    tmp_out.close()

    try:
        sound = AudioSegment.from_file(tmp_in_path)
        sound = sound.set_frame_rate(16000).set_channels(1).set_sample_width(2)
        sound.export(tmp_out_path, format="wav")
        return tmp_out_path
    finally:
        try:
            if os.path.exists(tmp_in_path):
                os.unlink(tmp_in_path)
        except Exception:
            pass
