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
from audio_settings import get_selected_device, get_recording_duration


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
        if ("FiiO" in mics[i].name) and "Loopback" not in str(mics[i].name):
            print(f"{i}: {mics[i].name}")
            return mics[i]


def record(duration=5, save_path="output.wav"):
    # Получить выбранное пользователем устройство
    selected_device_info = get_selected_device()

    if selected_device_info is None:
        print("Устройство записи не выбрано. Отмена записи.")
        return False

    default_mic = selected_device_info["device"]
    print(f"Запись с устройства: {selected_device_info['name']}")

    sample_rate = 44100
    numFrames = int(sample_rate * duration)

    try:
        with default_mic.recorder(samplerate=sample_rate) as mic:
            print("Recording...")
            data = mic.record(numframes=numFrames)
            print("Done recording")

        wavfile.write(save_path, sample_rate, data)
        return True
    except Exception as e:
        print(f"Ошибка при записи: {e}")
        return False


def convert_to_mp3(input_path, output_path):
    # os.system(f"ffmpeg -i {input_path} -acodec libmp3lame -ab 128k {output_path}")
    # subprocess without output
    subprocess.run(["ffmpeg", "-i", input_path, "-acodec", "libmp3lame", "-ab", "128k", output_path],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    # print_devices()
    print(get_realtek())
