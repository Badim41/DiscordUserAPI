import mimetypes


def get_mimetype(file_path):
    # Получаем MIME-тип файла
    mime_type, _ = mimetypes.guess_type(file_path)

    # Если MIME-тип не определен, возвращаем 'unknown'
    return mime_type if mime_type is not None else 'unknown'