# DiscordUserAPI

Асинхронная Python-библиотека для управления пользовательским аккаунтом Discord (User API / Self-bot) через Discord Gateway (WebSocket) и HTTP API v9.

---

## Содержание

1. [Установка](#install)
2. [Быстрый старт](#quickstart)
3. [Инициализация клиента (`Client`)](#client-init)
   - [Параметры `Client`](#client-params)
   - [Устройства (`ClientDevice`) и статусы (`PresenceStatus`)](#devices-and-status)
4. [Обработка событий (Хэндлеры)](#handlers)
5. [Методы клиента](#methods)
   - [Сообщения и файлы](#messages)
   - [Голосовые сообщения](#voice-messages)
   - [Реакции и эмодзи](#reactions)
   - [Статус и активность (Rich Presence)](#activity)
   - [Слэш-команды и интерактивные компоненты](#slash-commands)
6. [Информация о текущем пользователе и серверах (`client.info`)](#client-info)
7. [Логирование и обработка ошибок](#logging-and-errors)

---

## 1. Установка <a name="install"></a>

Установите пакет напрямую из GitHub с помощью `pip`:

```bash
pip install git+https://github.com/Badim41/DiscordUserAPI.git
```

> **Примечание:** Для отправки голосовых сообщений (`send_voice`) используется библиотека `pydub`, которой требуется установленный в системе пакет **FFmpeg**.

---

## 2. Быстрый старт <a name="quickstart"></a>

```python
import asyncio
import discord_user
from discord_user.types import ClientDevice, PresenceStatus, DiscordMessage

client = discord_user.Client(
    secret_token="ВАШ_ТОКЕН_АВТОРИЗАЦИИ",
    status=PresenceStatus.ONLINE,
    device=ClientDevice.windows
)

@client.on_start
async def on_start():
    print(f"Аккаунт запущен: {client.info.username} (ID: {client.info.user_id})")

@client.message_handler
async def on_message(message: DiscordMessage):
    print(f"[{message.channel_id}] {message.author.username}: {message.text}")

    if message.text == "!ping":
        await client.send_message(
            chat_id=message.channel_id,
            text="Pong!",
            reply_message=message,
            replied_user=True
        )

if __name__ == "__main__":
    asyncio.run(client.start_polling())
```

---

## 3. Инициализация клиента (`Client`) <a name="client-init"></a>

```python
import discord_user
from discord_user.types.presence import PresenceStatus
from discord_user.types.device import ClientDevice

client = discord_user.Client(
    secret_token="Authorization_Token",
    status=PresenceStatus.ONLINE,
    device=ClientDevice.windows,
    afk=False,
    proxy_uri="socks5://user:password@127.0.0.1:1080",
    cookie=None
)
```

### Параметры `Client` <a name="client-params"></a>

| Параметр | Тип | По умолчанию | Описание |
| :--- | :--- | :--- | :--- |
| `secret_token` | `str` | *Обязательный* | Токен аккаунта (значение заголовка `Authorization` в запросах к `discord.com`). |
| `status` | `str` | `PresenceStatus.ONLINE` | Начальный статус присутствия аккаунта. |
| `device` | `dict` | `ClientDevice.windows` | Эмулируемое устройство для подключения к Discord Gateway. |
| `afk` | `bool` | `False` | Флаг неактивности (`AFK`). |
| `proxy_uri` | `str \| None` | `None` | Прокси для HTTP и WebSocket соединений (рекомендуется `socks5://...`). |
| `cookie` | `str \| None` | `None` | Дополнительный заголовок `Cookie` для HTTP-запросов. |

### Устройства (`ClientDevice`) и статусы (`PresenceStatus`) <a name="devices-and-status"></a>

**Доступные профили устройств (`discord_user.types.ClientDevice`):**
* `ClientDevice.windows` — браузер/клиент на Windows
* `ClientDevice.web` — веб-клиент
* `ClientDevice.macos` — клиент macOS
* `ClientDevice.linux` — клиент Linux
* `ClientDevice.android` — мобильный клиент Android (отображает иконку телефона)
* `ClientDevice.ios` — мобильный клиент iOS (отображает иконку телефона)

**Доступные статусы (`discord_user.types.PresenceStatus`):**
* `PresenceStatus.ONLINE` (`"online"`) — В сети
* `PresenceStatus.IDLE` (`"idle"`) — Неактивен
* `PresenceStatus.DND` (`"dnd"`) — Не беспокоить
* `PresenceStatus.INVISIBLE` (`"invisible"`) — Невидимый

---

## 4. Обработка событий (Хэндлеры) <a name="handlers"></a>

Библиотека предоставляет декораторы для подписки на события WebSocket-шлюза Discord:

```python
from discord_user.types import (
    DiscordMessage,
    SlashCommandMessage,
    Presence,
    EventType
)

# 1. Вызывается при успешной авторизации и получении события READY
@client.on_start
async def on_ready():
    print("Клиент готов к работе!")

# 2. Новое обычное сообщение (MESSAGE_CREATE)
@client.message_handler
async def on_new_message(message: DiscordMessage):
    print(f"Новое сообщение: {message.text}")

# 3. Редактирование сообщения (MESSAGE_UPDATE)
@client.message_update_handler
async def on_edit_message(message: DiscordMessage):
    print(f"Сообщение {message.message_id} изменено: {message.text}")

# 4. Ответ бота на слэш-команду (MESSAGE_CREATE с interaction_metadata)
@client.slash_command_handler
async def on_slash_response(message: SlashCommandMessage):
    print(f"Ответ на команду /{message.interaction_metadata.name} от {message.author.username}")

# 5. Обновление статуса/активности пользователей (PRESENCE_UPDATE)
@client.status_update_handler
async def on_presence(presence: Presence):
    if presence.user.username:
        print(f"Пользователь {presence.user.username} изменил статус на {presence.status}")

# 6. Изменение состояния голосового канала (VOICE_STATE_UPDATE)
@client.voice_status_handler
async def on_voice_state(data: dict):
    print("Обновление голосового статуса:", data)

# 7. Универсальный обработчик любых событий по коду из EventType
@client.event_handler(EventType.MESSAGE_REACTION_ADD)
async def on_reaction_add(data: dict):
    print("Добавлена реакция:", data)
```

> Полный список кодов событий доступен в классе `discord_user.types.EventType` (например: `SESSIONS_REPLACE`, `INTERACTION_MODAL_CREATE`, `GUILD_MEMBER_UPDATE`, `MESSAGE_DELETE`, `RELATIONSHIP_ADD` и др.).

---

## 5. Методы клиента <a name="methods"></a>

### Сообщения и файлы <a name="messages"></a>

#### Отправка сообщения (`send_message`)
```python
msg = await client.send_message(
    chat_id="123456789012345678",
    text="Привет с вложением!",
    file_path="path/to/image.png",       # Опционально: путь к файлу
    reply_message=other_discord_message, # Опционально: объект DiscordMessage для ответа
    replied_user=True                    # Упоминать ли автора при ответе
)
```

#### Получение истории сообщений (`get_messages`)
```python
messages = await client.get_messages(chat_id="123456789012345678", limit=20)
for msg in reversed(messages):
    print(f"{msg.author.global_name}: {msg.text}")
```

#### Удаление сообщения и статус «печатает...» (`delete_message`, `send_typing`)
```python
# Показать индикатор набора текста ("печатает...")
await client.send_typing(chat_id="123456789012345678")

# Удалить сообщение по его ID
await client.delete_message(chat_id="123456789012345678", message_id="987654321098765432")
```

---

### Голосовые сообщения <a name="voice-messages"></a>

Метод `send_voice` автоматически конвертирует аудиофайл, вычисляет его длительность, генерирует звуковую волну (`waveform`) и отправляет файл как нативное голосовое сообщение Discord:

```python
voice_msg = await client.send_voice(
    chat_id="123456789012345678",
    audio_path="voice_note.ogg" # Поддерживаются любые форматы, доступные FFmpeg (mp3, wav, ogg)
)
```

---

### Реакции и эмодзи <a name="reactions"></a>

В качестве реакции можно передать как обычный Unicode-символ (`str`), так и кастомный эмодзи сервера через класс `Emoji`:

```python
from discord_user.types import Emoji

# Установка обычной реакции
await client.set_reaction(chat_id="123456789012345678", message_id="111222333", reaction="🔥")

# Установка кастомного эмодзи из строки вида <:name:id> или <a:name:id>
custom_emoji = Emoji.from_str("<a:Poppop_Faradey:1296351664411770892>")
await client.set_reaction(chat_id="123456789012345678", message_id="111222333", reaction=custom_emoji)

# Удаление своей реакции
await client.remove_reaction(chat_id="123456789012345678", message_id="111222333", reaction="🔥")
```

Для извлечения всех кастомных эмодзи из текста сообщения можно использовать утилиту `extract_discord_emojis`:
```python
from discord_user.utils.re_str import extract_discord_emojis

emojis = extract_discord_emojis("Привет <:smile:123456789012345678>!")
```

---

### Статус и активность (Rich Presence) <a name="activity"></a>

Для изменения статуса и активности во время работы используется метод `change_activity`. По умолчанию встроено ограничение частоты вызовов (не чаще раза в 20 секунд, отключается флагом `ignore_limit=True`).

#### 1. Пользовательский текстовый статус (`CustomStatus`)
```python
from discord_user.types import CustomStatus, PresenceStatus

custom_status = CustomStatus(state="Пишу код на Python")
await client.change_activity(activity=custom_status, status=PresenceStatus.ONLINE)
```

#### 2. Расширенная активность с картинками и кнопками (`Activity`)
```python
import datetime
from discord_user.types import Activity, ActivityType, PresenceStatus

now_ms = int(datetime.datetime.now().timestamp()) * 1000

activity_data = {
    "id": "3c5be2936bd6924c",
    "created_at": now_ms,
    "name": "DiscordUserAPI",
    "details": "Разработка бота",
    "state": "В процессе...",
    "type": ActivityType.PLAYING, # PLAYING, STREAMING, LISTENING, WATCHING, CUSTOM, COMPETING
    "assets": {
        "large_image": "mp:external/mZs-Vaj1ttjVMod8xlxrH1oTOZ8geVgQlDhiCKvaXY0/https/yellowfire.ru/uploaded_files/ukushu_1.gif",
        "large_text": "Подсказка при наведении"
    },
    "timestamps": {
        "start": now_ms
    },
    "buttons": ["GitHub", "Сайт"],
    "application_id": "544816254435983360",
    "metadata": {
        "button_urls": [
            "https://github.com/Badim41/DiscordUserAPI",
            "https://yellowfire.ru"
        ]
    }
}

activity = Activity.from_json(activity_data)
await client.change_activity(activity=activity, status=PresenceStatus.IDLE, ignore_limit=True)
```

#### 3. Сброс активности (`NoActivity`)
```python
from discord_user.types import NoActivity, PresenceStatus

await client.change_activity(activity=NoActivity(), status=PresenceStatus.ONLINE, ignore_limit=True)
```

---

### Слэш-команды и интерактивные компоненты <a name="slash-commands"></a>

Для вызова слэш-команд, нажатия на кнопки (`type: 3`) или отправки модальных окон (`type: 5`) используется класс `SlashCommand` и метод `client.use_slash_command`:

```python
from discord_user.types.slash_command import SlashCommand

raw_interaction_payload = {
    "type": 2,
    "application_id": "315926021457051650",
    "guild_id": "1069196218447691836",
    "channel_id": "1070713643387330590",
    "data": {
        "version": "956435492398841859",
        "id": "956435492398841858",
        "name": "bump",
        "type": 1,
        "options": [],
        "attachments": []
    },
    "analytics_location": "slash_ui"
}

command = SlashCommand.from_dict(
    json_data=raw_interaction_payload,
    session_id=client.info.session_id
)

await client.use_slash_command(command)
```

---

## 6. Информация о текущем пользователе и серверах (`client.info`) <a name="client-info"></a>

После срабатывания события `READY` (внутри и после `@client.on_start`) в объекте `client.info` (`SelfUserInfo`) доступна подробная информация об аккаунте:

* `client.info.user_id` (`str`) — ID текущего пользователя.
* `client.info.username` (`str`) — Имя пользователя (юзернейм).
* `client.info.global_name` (`str`) — Отображаемое имя.
* `client.info.email` / `client.info.phone` — Привязанная почта и телефон.
* `client.info.is_nitro` (`bool`) — Наличие подписки Discord Nitro.
* `client.info.session_id` (`str`) — ID текущей сессии Gateway (необходим для отправки `SlashCommand`).
* `client.info.friends_id` (`List[str]`) — Список ID друзей.
* `client.info.guilds` (`Dict[str, Guild]`) — Словарь серверов (`Guild`), где ключом является `guild_id`. Внутри каждого объекта `Guild` доступны:
  * `guild.name`, `guild.owner_id`, `guild.member_count`, `guild.description`
  * `guild.channels` (`Dict[str, Channel]`) — текстовые, голосовые, форумные и трибунные каналы сервера
  * `guild.roles` (`Dict[str, Role]`) — роли сервера
  * `guild.emojis` (`Dict[str, Emoji]`) — кастомные эмодзи сервера
  * `guild.stickers` (`Dict[str, Sticker]`) — стикеры сервера

---

## 7. Логирование и обработка ошибок <a name="logging-and-errors"></a>

### Настройка уровня логирования
По умолчанию логгер выводит только ошибки (`logging.ERROR`). Чтобы включить подробный вывод (`DEBUG` или `INFO`), используйте `set_logging_level`:

```python
import logging
from discord_user.global_logger.logs import set_logging_level

set_logging_level(logging.DEBUG)
```

### Исключения (`discord_user.errors`)
* `DiscordUserException` — базовый класс исключений библиотеки.
* `DiscordRequestError` — ошибка при выполнении HTTP-запроса к API Discord (неверный статус ответа, ошибка загрузки вложения и т.д.).
* `InvalidTokenError` — передан недействительный токен авторизации (код закрытия сокета `4004`).
