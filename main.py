import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import io
import pygame
from pedalboard import Pedalboard, Reverb
from pedalboard.io import AudioFile

class ModernMusicStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("SLVspeed")
        self.root.geometry("450x600")
        self.root.configure(bg="#0f0f0f") # Deep black background

        # Initialize Pygame for the in-app player
        pygame.mixer.init()
        
        self.file_path = None
        self.is_playing = False

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TProgressbar", thickness=10, troughcolor='#1a1a1a', background='#1db954')

    def create_widgets(self):
        # Header
        tk.Label(self.root, text="SLVspeed", fg="#1db954", bg="#0f0f0f", font=("Helvetica", 24, "bold")).pack(pady=30)

        # Import Section
        self.btn_import = tk.Button(self.root, text="IMPORT TRACK", command=self.import_song, 
                                   bg="#1db954", fg="white", font=("Helvetica", 10, "bold"),
                                   padx=20, pady=10, relief="flat", activebackground="#17a34a")
        self.btn_import.pack(pady=10)

        self.lbl_file = tk.Label(self.root, text="No track loaded", fg="#888888", bg="#0f0f0f", font=("Helvetica", 9))
        self.lbl_file.pack()

        # Controls Container
        ctrl_frame = tk.Frame(self.root, bg="#1a1a1a", padx=20, pady=20)
        ctrl_frame.pack(fill="x", padx=30, pady=20)

        # Speed Slider
        tk.Label(ctrl_frame, text="SPEED & PITCH", fg="#eeeeee", bg="#1a1a1a", font=("Helvetica", 9, "bold")).pack(anchor="w")
        self.speed_slider = tk.Scale(ctrl_frame, from_=0.5, to=1.2, resolution=0.01, orient="horizontal", 
                                    bg="#1a1a1a", fg="#1db954", highlightthickness=0, troughcolor="#333")
        self.speed_slider.set(0.85)
        self.speed_slider.pack(fill="x", pady=(0, 15))

        # Reverb Slider
        tk.Label(ctrl_frame, text="REVERB INTENSITY", fg="#eeeeee", bg="#1a1a1a", font=("Helvetica", 9, "bold")).pack(anchor="w")
        self.reverb_slider = tk.Scale(ctrl_frame, from_=0.0, to=1.0, resolution=0.05, orient="horizontal", 
                                     bg="#1a1a1a", fg="#1db954", highlightthickness=0, troughcolor="#333")
        self.reverb_slider.set(0.4)
        self.reverb_slider.pack(fill="x")

        # In-App Player Buttons
        play_frame = tk.Frame(self.root, bg="#0f0f0f")
        play_frame.pack(pady=10)

        self.btn_preview = tk.Button(play_frame, text="▶ PREVIEW", command=self.toggle_preview, 
                                    bg="#333333", fg="white", font=("Helvetica", 9, "bold"), state="disabled")
        self.btn_preview.pack(side="left", padx=5)

        # Export Button
        self.btn_export = tk.Button(self.root, text="DOWNLOAD FINAL TRACK", command=self.start_export, 
                                   bg="#0f0f0f", fg="#1db954", font=("Helvetica", 10, "bold"),
                                   highlightbackground="#1db954", highlightthickness=2, relief="flat", state="disabled")
        self.btn_export.pack(pady=20, fill="x", padx=80)

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")

    def import_song(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if self.file_path:
            self.lbl_file.config(text=os.path.basename(self.file_path))
            self.btn_preview.config(state="normal")
            self.btn_export.config(state="normal")

    def toggle_preview(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.btn_preview.config(text="▶ PREVIEW")
            self.is_playing = False
        else:
            threading.Thread(target=self.play_effect_live, daemon=True).start()

    def play_effect_live(self):
        # Process a small 30-second chunk for preview
        try:
            self.btn_preview.config(text="⌛ LOADING...")
            with AudioFile(self.file_path) as f:
                audio = f.read(f.samplerate * 30) # Read first 30 seconds
                samplerate = f.samplerate

            board = Pedalboard([Reverb(room_size=0.75, wet_level=self.reverb_slider.get())])
            effected_audio = board(audio, samplerate)
            
            # Temporary WAV for playback
            temp_preview = "preview.wav"
            with AudioFile(temp_preview, 'w', int(samplerate * self.speed_slider.get()), effected_audio.shape[0]) as f:
                f.write(effected_audio)

            pygame.mixer.music.load(temp_preview)
            pygame.mixer.music.play()
            self.is_playing = True
            self.btn_preview.config(text="■ STOP")
        except Exception as e:
            messagebox.showerror("Player Error", f"Could not play preview: {e}")

    def start_export(self):
        self.btn_export.config(state="disabled", text="RENDERING...")
        self.progress.pack(pady=10)
        self.progress.start()
        threading.Thread(target=self.export_track, daemon=True).start()

    def export_track(self):
        try:
            save_path = filedialog.asksaveasfilename(defaultextension=".wav")
            if save_path:
                with AudioFile(self.file_path) as f:
                    audio = f.read(f.frames)
                    samplerate = f.samplerate

                board = Pedalboard([Reverb(room_size=0.75, wet_level=self.reverb_slider.get())])
                effected_audio = board(audio, samplerate)
                
                with AudioFile(save_path, 'w', int(samplerate * self.speed_slider.get()), effected_audio.shape[0]) as f:
                    f.write(effected_audio)
                
                messagebox.showinfo("Done", "Vibe exported successfully!")
        finally:
            self.progress.stop()
            self.progress.pack_forget()
            self.btn_export.config(state="normal", text="DOWNLOAD FINAL TRACK")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernMusicStudio(root)
    root.mainloop()