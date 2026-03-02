# SLVspeed
🌊 SLVspeed: Slowed + Reverb/Speed up Generator
SLVspeed is a modern, high-fidelity desktop application designed to transform any song into a "Slowed + Reverb" masterpiece. Unlike standard players that just change playback speed, VibeStudio uses professional-grade digital signal processing to drop the pitch and tempo smoothly while adding atmospheric depth.

✨ Features
Smooth Pitch/Speed Shift: Uses sample-rate reduction to ensure the "slowed" effect sounds deep and natural, not glitchy.

High-Fidelity Reverb: Powered by the Pedalboard engine for studio-quality room simulation.

Modern UI: Built with a dark-themed, responsive interface.

In-App Export: Process and save your tracks directly to .wav format.

🚀 Installation
1. Prerequisites

Download Python 3.12/3.14 from python.org.

Important: Ensure "Add Python to PATH" is checked during installation.

2. Install Dependencies
Open your terminal and run:

FOR 3.14:
python -m pip install pygame-ce

FOR 3.12 AND BELOW:
pip install pygame

pip install customtkinter pedalboard

3. Run the App
Bash
python main.py
🛠️ How it Works
Import: Select any .mp3 or .wav file.

Adjust: Use the sliders to find your vibe.

Classic Slowed: Set Speed to 0.80x - 0.85x.

Deep Reverb: Set Intensity to 0.50 or higher.

Export: Click "SAVE" to render the final audio. The app uses a background thread to ensure the UI remains responsive during processing.

📜 Technical Credits
UI: CustomTkinter

DSP Engine: Pedalboard by Spotify

Audio Output: winsound (Windows Native)
