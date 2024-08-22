import logging
import sys

# Создаем StreamHandler и задаем ему начальный уровень
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Инициализируем логгер и добавляем хендлер
_log = logging.getLogger(__name__)
_log.setLevel(logging.DEBUG)
_log.addHandler(console_handler)

# Отключаем пропагирование сообщений на более высокие уровни
_log.propagate = False

def set_logging_level(level):
    _log.setLevel(level)

    # Изменяем уровень хендлера, если нужно
    for handler in _log.handlers:
        handler.setLevel(level)