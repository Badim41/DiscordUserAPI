import re


def extract_discord_emojis(text):
    # Регулярное выражение для поиска эмоджи
    emoji_pattern = r'<:\w+:\d+>'

    emojis = re.findall(emoji_pattern, text)

    return emojis