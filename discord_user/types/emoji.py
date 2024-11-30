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
        if self.animated:
            return f"https://cdn.discordapp.com/emojis/{self.id}.gif?animated=true"
        else:
            return f"https://cdn.discordapp.com/emojis/{self.id}.webp?size=4096"

    @staticmethod
    def from_str(emoji_str):
        emoji = Emoji()

        pattern_2 = r"<(a?):(\w+):(\d+)>"

        match_2 = re.search(pattern_2, emoji_str)
        if match_2:
            emoji.animated = bool(match_2.group(1))  # Если "a" есть, это анимированный эмодзи
            emoji.name = match_2.group(2)  # Имя эмоджи
            emoji.id = match_2.group(3)  # ID эмоджи
        else:
            emoji.name = None
            emoji.id = None
            emoji.animated = False

        return emoji

    def __repr__(self):
        return f"Emoji(name={self.name}, id={self.id}, animated={self.animated})"

if __name__ == '__main__':
    str_1 = "hi <a:Poppop_Faradey:1296351664411770892> 123"
    print(Emoji.from_str(str_1))
    str_2 = "hi <:Poppop_Faradey:1296351664411770892> 123"
    print(Emoji.from_str(str_2))