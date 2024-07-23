class DiscordUserException(Exception):
    """Базовая ошибка с библиотекой DiscordUserAPI
    """

class SlashCommandException(DiscordUserException):
    """Ошибка при выполнении слэш-команды"""

