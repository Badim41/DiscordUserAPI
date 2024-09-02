import re
from typing import List

from ..types import Emoji


def extract_discord_emojis(text) -> List[Emoji]:
    # Регулярное выражение для поиска эмоджи
    emoji_pattern = r'<:\w+:\d+>'

    emojis_str = re.findall(emoji_pattern, text)

    return [Emoji.from_str(emoji_str) for emoji_str in emojis_str]