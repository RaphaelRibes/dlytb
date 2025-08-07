import sys
import os
import subprocess
import re
import argparse
from pytubefix import YouTube

def sanitize_filename(title, extension):
    """Nettoie un titre pour en faire un nom de fichier sûr."""
    sanitized = re.sub(r'[\\/*?:"<>|]', "", title)
    sanitized = sanitized.replace(" ", "_")
    return f"{sanitized}.{extension}"

def run_ffmpeg_command(command, action_desc, progress_callback=None):
    """Exécute une commande FFmpeg et gère les erreurs de manière détaillée."""
    try:
        if progress_callback:
            progress_callback(f"{action_desc}...")
        else:
            print(f"{action_desc}...")
            
        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
    except subprocess.CalledProcessError as e:
        error_message = (
            f"\n--- ERREUR FFmpeg ---\n"
            f"La commande a échoué avec le code : {e.returncode}\n"
            f"Commande exécutée : {' '.join(e.cmd)}\n"
            f"\n--- Sortie d'erreur de FFmpeg (stderr) ---\n"
            f"{e.stderr}\n"
            f"---------------------------------"
        )
        if progress_callback:
            progress_callback(error_message)
        else:
            print(error_message)
        raise

def telecharger_audio_seulement(url, audio_format, num_cores, output_dir, progress_callback=None):
    """Télécharge et convertit une piste audio depuis une URL YouTube."""
    try:
        yt = YouTube(url)
        if progress_callback:
            progress_callback(f"Préparation de l'audio pour : {yt.title}")

        audio_stream = yt.streams.get_audio_only()
        if not audio_stream:
            message = "Aucun flux audio trouvé."
            if progress_callback:
                progress_callback(message)
            else:
                print(message)
            return

        os.makedirs(output_dir, exist_ok=True)
        
        if progress_callback:
            progress_callback("Téléchargement du flux audio...")
        temp_audio_path = audio_stream.download(filename="temp_audio_file.temp")
        if progress_callback:
            progress_callback("Téléchargement terminé.")

        output_filename = sanitize_filename(yt.title, audio_format)
        output_filepath = os.path.join(output_dir, output_filename)
        
        if audio_format == 'm4a':
            command = ['ffmpeg', '-i', temp_audio_path, '-c:a', 'copy', '-y', output_filepath]
            run_ffmpeg_command(command, f"Copie du flux en '{output_filepath}'", progress_callback)
        else: # mp3
            command = ['ffmpeg', '-i', temp_audio_path, '-vn', '-q:a', '0', '-threads', str(num_cores), '-y', output_filepath]
            run_ffmpeg_command(command, f"Conversion en '{output_filepath}'", progress_callback)
        
        os.remove(temp_audio_path)
        
        success_message = f"\nFichier audio enregistré : {output_filepath}"
        if progress_callback:
            progress_callback(success_message)
        else:
            print(success_message)

    except Exception as e:
        error_message = f"\nUne erreur générale est survenue: {e}"
        if progress_callback:
            progress_callback(error_message)
        else:
            print(error_message)
        # Re-raise the exception so the calling UI can handle it if needed
        raise

def telecharger_haute_qualite_video(url, output_dir, progress_callback=None):
    """Télécharge une vidéo en haute qualité et fusionne l'audio."""
    try:
        yt = YouTube(url)
        if progress_callback:
            progress_callback(f"Préparation de la vidéo pour : {yt.title}")

        video_stream = yt.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc().first()
        audio_stream = yt.streams.get_audio_only()
        
        if not video_stream or not audio_stream:
             message = "Flux vidéo/audio requis non trouvé."
             if progress_callback:
                 progress_callback(message)
             else:
                 print(message)
             return

        os.makedirs(output_dir, exist_ok=True)
        
        if progress_callback:
            progress_callback("Téléchargement du flux vidéo...")
        temp_video_path = video_stream.download(filename="temp_video_file.temp")
        
        if progress_callback:
            progress_callback("Téléchargement du flux audio...")
        temp_audio_path = audio_stream.download(filename="temp_audio_file.temp")
        
        if progress_callback:
            progress_callback("Téléchargements terminés.")
        
        output_filename = sanitize_filename(yt.title, "mp4")
        output_filepath = os.path.join(output_dir, output_filename)
        
        command = ['ffmpeg', '-i', temp_video_path, '-i', temp_audio_path, '-c:v', 'copy', '-c:a', 'copy', '-y', output_filepath]
        run_ffmpeg_command(command, f"Fusion en '{output_filepath}'", progress_callback)

        os.remove(temp_video_path)
        os.remove(temp_audio_path)
        
        success_message = f"\nVidéo enregistrée : {output_filepath}"
        if progress_callback:
            progress_callback(success_message)
        else:
            print(success_message)

    except Exception as e:
        error_message = f"\nUne erreur générale est survenue: {e}"
        if progress_callback:
            progress_callback(error_message)
        else:
            print(error_message)
        # Re-raise the exception so the calling UI can handle it if needed
        raise

# This block will only run when the script is executed directly
# e.g., `python dlytb.py ...`
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Télécharge des vidéos ou des pistes audio depuis YouTube.")
    parser.add_argument("output_path", help="Chemin de sortie (utilisez '.' pour le répertoire courant).")
    parser.add_argument("url", help="L'URL de la vidéo YouTube.")
    parser.add_argument("-a", "--audio", action="store_true", help="Télécharger uniquement l'audio.")
    parser.add_argument("-f", "--format", type=str, default="mp3", choices=['mp3', 'm4a'], help="Format audio (défaut: mp3).")
    parser.add_argument("-c", "--cores", type=int, default=0, help="Coeurs CPU pour l'encodage MP3 (0=auto).")
    
    args = parser.parse_args()
    
    # Simple callback function to print progress messages to the console
    def console_progress_callback(message):
        print(message)

    try:
        if args.audio:
            telecharger_audio_seulement(args.url, args.format, args.cores, args.output_path, console_progress_callback)
        else:
            telecharger_haute_qualite_video(args.url, args.output_path, console_progress_callback)
    except Exception as e:
        # The functions already print detailed errors, but we can catch any final issues.
        print(f"L'opération a échoué.")
