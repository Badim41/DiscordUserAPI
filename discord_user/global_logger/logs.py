import logging
import sys

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
console_handler.stream = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

logging.basicConfig(level=logging.DEBUG, handlers=[console_handler])

_log = logging.getLogger(__name__)