import asyncio
import datetime

import discord_user
from discord_user import secret
from discord_user.types import Activity, ActivityType, PresenceStatus, ClientDevice

# например запуска с прокси и устройством
client = discord_user.Client(secret_token=secret.auth_token_discord, device=ClientDevice.web)

@client.on_start
async def on_start():
    print("Пользователь запущен")

    # JSON данные для создания активности
    json_data = {
        'id': 'ed52e7003b57bc8',
        'created_at': 1723184107714,
        'name': 'на фенька',
        'type': ActivityType.WATCHING,
        'assets': {
            'large_image': 'mp:attachments/1160759712900468839/1272141863276515378/trickmint.gif?ex=66b9e5ef&is=66b8946f&hm=3f093d3ec6bf5ea6ad68f1a20142832c27858672b5c126a2fc48174fea0e564a&'
        },
        "timestamps": {
            "start": int(datetime.datetime.now().timestamp())
        },
    }

    # json_data = {
    #     'id': 'ed52e7003b57bc8',
    #     'created_at': 1723184107714,
    #     'name': 'сон',
    #     'type': ActivityType.WATCHING,
    #     'assets': {
    #         'large_image': 'mp:emojis/1212496120660365444.webp?format=webp&width=60&height=60'
    #     }
    # }

    # Создание объекта Activity
    activity = Activity.from_json(json_data)

    # Установка активности пользователя
    await client.change_activity(activity=activity, status=PresenceStatus.IDLE)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(client.start_polling())
