import os
import sys

try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    base_path = sys._MEIPASS
except AttributeError:
    base_path = os.path.abspath(".")

import soundcard as sc
from scipy.io import wavfile
import subprocess


def print_devices():
    mics = sc.all_microphones(include_loopback=True)

    for i in range(len(mics)):
        try:
            print(f"{i}: {mics[i].name}")
        except Exception as e:
            print(e)


def get_realtek():
    mics = sc.all_microphones(include_loopback=True)
    for i in range(len(mics)):
        if "Realtek(R) Audio" in mics[i].name:
            return mics[i]


def record(duration=5, save_path="output.wav"):
    # mics = sc.all_microphones(include_loopback=True)
    # default_mic = mics[1]

    default_mic = get_realtek()

    sample_rate = 44100
    numFrames = int(sample_rate * duration)

    with default_mic.recorder(samplerate=sample_rate) as mic:
        print("Recording...")
        data = mic.record(numframes=numFrames)
        print("Done recording")

    wavfile.write(save_path, sample_rate, data)


def convert_to_mp3(input_path, output_path):
    # os.system(f"ffmpeg -i {input_path} -acodec libmp3lame -ab 128k {output_path}")
    # subprocess without output
    subprocess.run(["ffmpeg", "-i", input_path, "-acodec", "libmp3lame", "-ab", "128k", output_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    print_devices()
