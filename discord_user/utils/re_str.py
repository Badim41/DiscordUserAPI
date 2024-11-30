import re
from typing import List

from ..types import Emoji


def extract_discord_emojis(text) -> List[Emoji]:
    emoji_pattern = r'<a?:\w+:\d+>'
    emojis = re.findall(emoji_pattern, text)

    return [Emoji.from_str(emoji_str) for emoji_str in emojis]
