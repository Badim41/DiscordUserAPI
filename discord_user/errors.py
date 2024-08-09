class DiscordUserException(Exception):
    """Базовая ошибка с библиотекой DiscordUserAPI
    """

class DiscordRequestError(DiscordUserException):
    """Ошибка при выполнении запроса"""
