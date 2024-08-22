import asyncio
import datetime
import sys

import discord_user
import secret
from discord_user.types import Activity, ActivityType, PresenceStatus, ClientDevice, EventType

# например запуска с прокси и устройством
client = discord_user.Client(secret_token=secret.auth_token_discord, device=ClientDevice.android, afk=False)

# JSON данные для создания активности
json_data = {
    'id': 'ed52e7003b57bc8',
    'created_at': int(datetime.datetime.now().timestamp()) * 1000,
    'name': 'на фенька и гладит его',
    'type': ActivityType.WATCHING,
    'assets': {
        'large_image': 'mp:attachments/1076241932201762906/1268700026729926777/image.png?ex=66c5c439&is=66c472b9&hm=569461e6a51993d762cdfa73accc1a87459452a2a94df2f507be032e71fd706e&'
    },
    "timestamps": {
        "start": int(datetime.datetime.now().timestamp()) * 1000
    },
}

# json_data = {
#     'id': 'ed52e7003b57bc8',
#     'created_at': int(datetime.datetime.now().timestamp()),
#     'name': 'на пили',
#     'type': ActivityType.WATCHING,
#     'assets': {
#         'large_image': 'mp:attachments/1203510398100447243/1275212248138121237/homer-simpson.gif?ex=66c51174&is=66c3bff4&hm=903a49089dceface9febf8e8a875d72962722657b67baa5a7a8d8019eb6d35d9&'
#     },
#     "timestamps": {
#         "start": int(datetime.datetime.now().timestamp()) * 1000
#     }
# }

# json_data = {
#     'id': 'ed52e7003b57bc8',
#     'created_at': 1723184107714,
#     'name': 'новое видео Фарадея',
#     'type': ActivityType.WATCHING,
#     'assets': {
#         'large_image': 'mp:emojis/1212496120660365444.webp?format=webp&width=60&height=60'
#     }
# }

# Создание объекта Activity
activity = Activity.from_json(json_data)


@client.event_handler(EventType.SESSIONS_REPLACE)
async def on_session_replace(data):
    print("session update:", data)
    # Установка активности пользователя
    await client.change_activity(activity=activity, status=PresenceStatus.IDLE)


@client.on_start
async def on_start():
    print("Пользователь запущен")
    # Установка активности пользователя
    await client.change_activity(activity=activity, status=PresenceStatus.IDLE)


if __name__ == '__main__':
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.get_event_loop().run_until_complete(client.start_polling())
