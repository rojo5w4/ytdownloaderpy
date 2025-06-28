# importar librerias
# este archivo si se lo pase a una ia para hacer correciones del otro archivo lo demas si lo hice yo JAJAJ
import os
import yt_dlp
print(" hecho por jesus david simosa ")

# verificar si la carpeta de descarga existe, si no, crearla
carpeta_descargas = "Elementos Descargados"
if not os.path.exists(carpeta_descargas):
    os.makedirs(carpeta_descargas)


# configuracion para la gui y el porcentaje de la descarga
def progress_hook_for_gui(d, gui_update_callback=None):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes', d.get('total_bytes_estimate', 0))
        downloaded_bytes = d.get('downloaded_bytes', 0)
        percent = (downloaded_bytes / total_bytes) * 100 if total_bytes > 0 else 0
        speed_str = d.get('_speed_str', 'N/A')
        eta_str = d.get('_eta_str', 'N/A')
        status_text = f"Descargando: {d['_percent_str']} de {d['_total_bytes_str']} a {speed_str} ETA {eta_str}"

        if gui_update_callback:
            gui_update_callback(percent, status_text)

# informar estado de la descarga
    elif d['status'] == 'finished': 
        if gui_update_callback:
            gui_update_callback(100, "Descarga Finalizada, post-procesando...") 
    elif d['status'] == 'error': 
        if gui_update_callback:
            gui_update_callback(0, "Se produjo un error en la descarga ")

# definir la configuracion de descarga
def start_download_process(url, format_choice, gui_update_callback=None):
    ydl_opts_base = {
        'noplaylist': True,
        'progress_hooks': [lambda d: progress_hook_for_gui(d, gui_update_callback)],
        'outtmpl': os.path.join(carpeta_descargas, '%(title)s.%(ext)s'),
    }

    ydl_opts_final = {}

# opciones de descarga dinamicas, permitir si descargar audio o video

# el usuario eligio audio
    if format_choice == 'audio':
        ydl_opts_final = {
            **ydl_opts_base, 
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
# el usuario eligio video
    elif format_choice == 'video':
        ydl_opts_final = {
            **ydl_opts_base,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        }
    else:
        if gui_update_callback:
            gui_update_callback(0, "error: formato de descarga no válido.")
        return False, "formato no válido, elige audio o video."
# progreso de la descarga
    try:
        if gui_update_callback:
            gui_update_callback(0, f"iniciando descarga de: {url}...")

        with yt_dlp.YoutubeDL(ydl_opts_final) as ydl:
            info_dict = ydl.extract_info(url, download=True) 
            title_downloaded = info_dict.get('title', 'Video sin título')
            return True, title_downloaded 
# manejo de errores            
    except yt_dlp.DownloadError as e:
        return False, f"se produjo un error durante la descarga: {e}"
    except Exception as e:
        return False, f"Se produjo un error (vete a saber cual): {e}" 
    finally:
        pass