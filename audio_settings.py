import json
import os
import soundcard as sc

SETTINGS_FILE = "audio_settings.json"


def get_default_settings():
    return {
        "selected_device_index": None,
        "selected_device_name": None,
        "recording_duration": 5  # длительность записи по умолчанию в секундах
    }


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return get_default_settings()
    return get_default_settings()


def save_settings(settings):
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)


def get_all_audio_devices():
    """Получить все доступные аудиоустройства"""
    devices = []
    mics = sc.all_microphones(include_loopback=True)

    for i, mic in enumerate(mics):
        try:
            devices.append({
                "index": i,
                "name": mic.name,
                "device": mic
            })
        except Exception as e:
            print(f"Ошибка при получении устройства {i}: {e}")

    return devices


def print_audio_devices():
    """Вывести список всех доступных аудиоустройств"""
    devices = get_all_audio_devices()
    print("\nДоступные аудиоустройства:")
    print("-" * 50)
    for device in devices:
        print(f"{device['index']}: {device['name']}")
    print("-" * 50)
    return devices


def select_audio_device():
    """Интерактивный выбор аудиоустройства"""
    devices = print_audio_devices()

    if not devices:
        print("Аудиоустройства не найдены!")
        return None

    while True:
        try:
            choice = input(f"\nВыберите устройство (0-{len(devices) - 1}) или 'q' для отмены: ")
            if choice.lower() == 'q':
                return None

            device_index = int(choice)
            if 0 <= device_index < len(devices):
                selected_device = devices[device_index]

                # Сохранить выбор
                settings = load_settings()
                settings["selected_device_index"] = device_index
                settings["selected_device_name"] = selected_device["name"]
                save_settings(settings)

                print(f"Выбрано устройство: {selected_device['name']}")
                return selected_device
            else:
                print("Неверный индекс устройства!")
        except ValueError:
            print("Введите корректный номер!")


def get_selected_device():
    """Получить выбранное устройство из настроек"""
    settings = load_settings()

    if settings["selected_device_index"] is None:
        print("Устройство не выбрано. Выберите устройство:")
        return select_audio_device()

    # Проверить, что устройство все еще доступно
    devices = get_all_audio_devices()
    device_index = settings["selected_device_index"]

    if device_index < len(devices):
        device = devices[device_index]
        if device["name"] == settings["selected_device_name"]:
            return device

    print(f"Ранее выбранное устройство '{settings['selected_device_name']}' недоступно.")
    print("Выберите новое устройство:")
    return select_audio_device()


def get_recording_duration():
    """Получить сохраненную длительность записи"""
    settings = load_settings()
    return settings.get("recording_duration", 5)


def set_recording_duration(duration):
    """Сохранить новую длительность записи"""
    if duration <= 0:
        print("Длительность должна быть больше 0 секунд!")
        return False

    settings = load_settings()
    settings["recording_duration"] = duration
    save_settings(settings)
    print(f"Длительность записи установлена: {duration} секунд")
    return True


def select_recording_duration():
    """Интерактивный выбор длительности записи"""
    current_duration = get_recording_duration()
    print(f"\nТекущая длительность записи: {current_duration} секунд")

    while True:
        try:
            choice = input("Введите новую длительность в секундах (или 'q' для отмены): ")
            if choice.lower() == 'q':
                return current_duration

            duration = float(choice)
            if set_recording_duration(duration):
                return duration
        except ValueError:
            print("Введите корректное число!")
