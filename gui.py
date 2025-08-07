# gui.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from dlytb import telecharger_audio_seulement, telecharger_haute_qualite_video

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("dlytb UI")
        self.geometry("500x300")

        # UI Elements
        self.url_label = ttk.Label(self, text="YouTube URL:")
        self.url_label.pack(pady=5)

        self.url_entry = ttk.Entry(self, width=60)
        self.url_entry.pack(pady=5)

        self.download_type = tk.StringVar(value="video")
        self.video_radio = ttk.Radiobutton(self, text="Vidéo (MP4)", variable=self.download_type, value="video")
        self.video_radio.pack(pady=2)
        self.audio_mp3_radio = ttk.Radiobutton(self, text="Audio (MP3)", variable=self.download_type, value="mp3")
        self.audio_mp3_radio.pack(pady=2)
        self.audio_m4a_radio = ttk.Radiobutton(self, text="Audio (M4A)", variable=self.download_type, value="m4a")
        self.audio_m4a_radio.pack(pady=2)

        self.download_button = ttk.Button(self, text="Télécharger", command=self.start_download)
        self.download_button.pack(pady=20)

        self.status_label = ttk.Label(self, text="Prêt.")
        self.status_label.pack(pady=10)

    def update_status(self, message):
        # Since this can be called from another thread, ensure it's thread-safe
        self.after(0, self.status_label.config, {'text': message})

    def start_download(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Erreur", "Veuillez entrer une URL.")
            return

        output_path = filedialog.askdirectory(title="Choisir un dossier de sauvegarde")
        if not output_path:
            return

        self.download_button.config(state=tk.DISABLED)
        self.update_status("Démarrage du téléchargement...")

        # Run the download in a separate thread to avoid freezing the UI
        # Pass the url and output_path as arguments to the target function
        thread = threading.Thread(target=self.run_download, args=(url, output_path))
        thread.start()

    # MODIFIED: The function now accepts the url and output_path arguments
    def run_download(self, url, output_path):
        download_type = self.download_type.get()
        
        try:
            if download_type == "video":
                telecharger_haute_qualite_video(url, output_path, self.update_status)
            else: # mp3 or m4a
                telecharger_audio_seulement(url, download_type, 0, output_path, self.update_status)
            
            # Use self.after to schedule the messagebox on the main thread
            self.after(0, lambda: messagebox.showinfo("Succès", "Téléchargement terminé !"))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Erreur", f"Une erreur est survenue:\n{e}"))
        finally:
            # Ensure the button is re-enabled on the main thread
            self.after(0, self.download_button.config, {'state': tk.NORMAL})
            self.update_status("Prêt.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
