# Discord Tools

Инструменты для работы с Discord, функции чат-ботов, генерация изображений, модерация текста, поиск в интернете, базы данных, перевод, таймеры.

1. [Установка](#section-1)
2. [DiscordUser](#section-2)
   1. [Базовый класс](#section-2.1)
   2. [Аргументы](#section-2.2)


## Установка <a name="section-1"></a>

Установите пакет с помощью pip:

```bash
pip install git+https://github.com/Badim41/DiscordUserAPI.git
```

# DiscordUser <a name="section-2"></a>
## Создание класса пользователя <a name="section-2.1"></a>
```python
import discord_user

client = discord_user.Client(secret_token="КЛЮЧ АККАУНТА")
# ключ аккаунта - значение из Bearer в запросе к disocrd.com
```

## Аргументы для создания <a name="section-2.2"></a>
```python
import discord_user
from discord_user.types.presence import PresenceStatus
from discord_user.types.device import ClientDevice

client = discord_user.Client(
    secret_token="КЛЮЧ АККАУНТА",
    default_guild_ids=[int, None], # Фильтр гильдий. None - личные сообщения
    status=PresenceStatus.ONLINE, # Статус (онлайн, офлайн ...)
    device=ClientDevice.windows, # Устройство
    afk=False, # afk
    proxy_uri = None # proxy (рекомендовано SOCK5)
)


```