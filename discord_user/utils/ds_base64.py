import base64

def encode_base64(input_string: str) -> str:
    # Преобразуем строку в байты
    bytes_input = input_string.encode('utf-8')
    # Кодируем байты в base64
    base64_bytes = base64.b64encode(bytes_input)
    # Преобразуем результат в строку
    base64_string = base64_bytes.decode('utf-8')
    return base64_string

def decode_base64(encoded_string: str) -> str:
    # Преобразуем строку в байты
    base64_bytes = encoded_string.encode('utf-8')
    # Декодируем base64 в байты
    bytes_output = base64.b64decode(base64_bytes)
    # Преобразуем результат в строку
    output_string = bytes_output.decode('utf-8')
    return output_string
