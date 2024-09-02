import base64
import os

from pydub import AudioSegment


def convert_audio(original_audio_path, audio_format):
    # Создание пути для сохранения нового WAV файла
    audio_path = original_audio_path.rsplit('.', 1)[0] + f'.{audio_format}'

    # Конвертация аудиофайла в формат
    audio = AudioSegment.from_file(original_audio_path)
    audio.export(audio_path, format=audio_format)

    return audio_path

def get_audio_duration(audio_path):
    return len(AudioSegment.from_file(audio_path)) / 1000.0  # продолжительность в секундах

def generate_waveform(audio_path):
    audio_path_ogg = convert_audio(original_audio_path=audio_path, audio_format="ogg")
    audio = AudioSegment.from_file(audio_path_ogg)
    # Преобразуем аудиофайл в массив чисел (samples)
    samples = audio.get_array_of_samples()
    # Уменьшаем количество точек до 256 для `waveform`
    waveform = [min(255, max(0, int(x / 256))) for x in samples[::max(1, len(samples) // 256)]]
    # print(waveform)
    # Кодируем в base64
    waveform_encoded = base64.b64encode(bytes(waveform)).decode('utf-8')

    if not audio_path_ogg == audio_path:
        os.remove(audio_path_ogg)

    return waveform_encoded