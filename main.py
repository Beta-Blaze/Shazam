import os
import subprocess
import requests
import zipfile as zipp
import shutil

from ShazamAPI import Shazam
from record import record, convert_to_mp3
from audio_settings import select_audio_device, get_selected_device, load_settings, get_recording_duration, select_recording_duration


def recognize(file_path):
    mp3_file_content_to_recognize = open(file_path, 'rb').read()
    shazam = Shazam(
        mp3_file_content_to_recognize,
    )
    recognize_generator = shazam.recognizeSong()
    return list(recognize_generator)


def pretty_print(res):
    if len(res) == 0 or len(res[0][1]) == 0 or 'track' not in res[0][1]:
        print("No results found, try again")
        return

    track = res[0][1]['track']
    title = track.get('title', '')
    subtitle = track.get('subtitle', '')
    images = track.get('images', {}).get('coverarthq', 'No image found')
    name = track.get('share', {}).get('subject', '')
    audio_url = track.get('hub', {}).get('actions', [{}, {}])[1].get('uri', '')
    text = track.get('sections', [{}])[1].get('text', 'No lyrics found')
    meta_title = track.get('sections', [{}])[0].get('metadata', [{}])[0].get('title',
                                                                             'No meta title found')
    meta_text = track.get('sections', [{}])[0].get('metadata', [{}])[0].get('text',
                                                                            'No meta text found')
    if len(track.get('sections', [{}])[0].get('metadata', [{}, {}, {}])) <= 1:
        label = "No label found"
        data = "No data found"
    else:
        label = track.get('sections', [{}])[0].get('metadata', [{}, {}])[1].get('text', 'No label found')
        data = track.get('sections', [{}])[0].get('metadata', [{}, {}, {}])[2].get('text', 'No data found')

    print(f"Title: {title}")
    print(f"Subtitle: {subtitle}")
    print(f"Images: {images}")
    print(f"Name: {name}")
    print(f"Audio URL: {audio_url}")
    print(f"Meta Title: {meta_title}")
    print(f"Meta Text: {meta_text}")
    print(f"Label: {label}")
    print(f"Data: {data}")
    if text == "No lyrics found":
        print(f"Lyrics: {text}")
    else:
        print("\n")
        print("Lyrics:\n", '\n'.join(text))


def main(duration, recording=True, input_file="output.mp3"):
    if recording:
        record(duration=duration, save_path="output.wav")
        try:
            os.remove("output.mp3")
        except Exception as e:
            pass
        convert_to_mp3("output.wav", "output.mp3")
    res = recognize(input_file)
    # print(res)
    pretty_print(res)
    os.remove("output.wav")
    os.remove("output.mp3")


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def download(url, file_name="DOWNLOADED_FILE"):
    r = requests.get(url, stream=True)

    total_size = int(r.headers.get('content-length', 0))
    block_size = 2048
    wrote = 0
    with open(file_name, 'wb') as f:
        for data in r.iter_content(block_size):
            wrote = wrote + len(data)
            f.write(data)
            printProgressBar(wrote, total_size, prefix='Progress:', suffix='Complete', length=50)
    if total_size != 0 and wrote != total_size:
        print("ERROR, something went wrong")


def ffmpeg_checker():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["ffprobe", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return
    except Exception as e:
        print("FFmpeg not found, downloading...")

    # windows ffmpeg download
    if os.name == 'nt':
        url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"

        download(url, "ffmpeg.zip")

        with zipp.ZipFile('ffmpeg.zip', 'r') as zip_ref:
            zip_ref.extractall()
        # find ffmpeg dir (ffmpeg-N.N.N.-essentials.zip)
        ffmpeg_dir = ""
        for i in os.listdir():
            if "ffmpeg-" in i:
                ffmpeg_dir = i
                break
        # move ffmpeg.exe and ffprobe.exe to root
        try:
            os.remove("ffmpeg.exe")
        except Exception as e:
            pass
        try:
            os.remove("ffprobe.exe")
        except Exception as e:
            pass

        os.rename(os.path.join(ffmpeg_dir, "bin", "ffmpeg.exe"), "ffmpeg.exe")
        os.rename(os.path.join(ffmpeg_dir, "bin", "ffprobe.exe"), "ffprobe.exe")
        os.remove('ffmpeg.zip')
        shutil.rmtree(ffmpeg_dir)
    # linux ffmpeg download
    else:
        os.system("sudo apt-get install ffmpeg")

    print("FFmpeg installed successfully!")
    print("Restart the program")
    input()
    exit()


def show_settings_menu():
    """Меню настроек"""
    while True:
        print("\n--- НАСТРОЙКИ ---")
        print("1. Изменить длительность записи")
        print("2. Выбрать аудиоустройство")
        print("3. Показать текущие настройки")
        print("0. Вернуться в главное меню")

        choice = input("Выберите опцию: ").strip()

        if choice == "1":
            select_recording_duration()

        elif choice == "2":
            device = select_audio_device()
            if device:
                print(f"Аудиоустройство изменено на: {device['name']}")
            else:
                print("Аудиоустройство не изменено")

        elif choice == "3":
            settings = load_settings()
            current_device = get_selected_device()
            current_duration = get_recording_duration()
            print(f"\nТекущие настройки:")
            print(f"Аудиоустройство: {current_device['name'] if current_device else 'Не выбрано'}")
            print(f"Длительность записи: {current_duration} секунд")

        elif choice == "0":
            break

        else:
            print("Неверный выбор, попробуйте снова")

    return None


if __name__ == "__main__":
    ffmpeg_checker()

    print("PC shazam")
    
    # Получить сохраненную длительность записи
    duration = get_recording_duration()

    # Показать текущие настройки при запуске
    current_device = get_selected_device()
    if current_device:
        print(f"Текущее аудиоустройство: {current_device['name']}")
    print(f"Длительность записи: {duration} секунд")

    while True:
        print("\nВыберите действие:")
        print("Enter - записать и распознать")
        print("'s' - настройки")
        print("'r' - распознать файл")
        print("'q' - выход")

        inp = input("Ввод: ").strip().lower()

        if inp == 'q':
            break
        elif inp == 's':
            show_settings_menu()
            # Обновить длительность после изменения настроек
            duration = get_recording_duration()
        elif inp == 'r':
            print("Распознавание файла")
            path = input("Введите путь к файлу (.mp3): ").strip()
            if os.path.exists(path):
                main(duration, input_file=path, recording=False)
            else:
                print("Файл не найден")
        else:
            main(duration)
        print("\n")
