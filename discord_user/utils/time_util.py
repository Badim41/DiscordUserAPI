import datetime
import time


def convert_timestamp_to_readable_time(timestamp_ms):
    # Преобразование метки времени из миллисекунд в секунды
    timestamp_s = timestamp_ms / 1000.0

    # Преобразование метки времени в объект datetime
    readable_time = datetime.datetime.fromtimestamp(timestamp_s)

    # Форматирование объекта datetime в читаемую строку
    readable_time_str = readable_time.strftime('%Y-%m-%d %H:%M:%S')

    return readable_time_str

def get_nonce() -> str:
    return str(int(time.time() * 734282690.97))