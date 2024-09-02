import re


class Emoji:
    def __init__(self, json_data=None):
        if json_data:
            self.id = json_data.get('id')
            self.name = json_data.get('name')

            self.roles = json_data.get('roles', [])  # Массив ролей, которые могут использовать эмоджи
            self.require_colons = json_data.get('require_colons', True)  # Требовать двоеточие для использования
            self.managed = json_data.get('managed', False)  # Управляется ли эмоджи
            self.available = json_data.get('available', True)  # Доступно ли эмоджи
            self.animated = json_data.get('animated', False)  # Является ли эмоджи анимированным
        else:
            self.id = None
            self.name = None
            self.roles = []
            self.require_colons = True
            self.managed = False
            self.available = True
            self.animated = False

    def get_url(self):
        return f"https://cdn.discordapp.com/emojis/{self.id}.webp?size=4096"

    @staticmethod
    def from_str(emoji_str):
        emoji = Emoji()

        pattern = r'<:(\w+):(\d+)>'
        match = re.match(pattern, emoji_str)
        if match:
            emoji.name = match.group(1)  # Имя эмоджи
            emoji.id = match.group(2)  # ID эмоджи
        else:
            raise ValueError("Строка не соответствует формату <:Имя:ID>")

        return emoji

    def __repr__(self):
        return f"Emoji(name={self.name}, id={self.id})"
