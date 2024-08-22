import asyncio
import datetime

import discord_user
from discord_user import secret
from discord_user.types import Activity, ActivityType, ClientDevice, PresenceStatus

# например запуска с прокси и устройством
client = discord_user.Client(secret_token=secret.auth_token_discord, device=ClientDevice.android, afk=True)

@client.on_start
async def on_start():
    print("Пользователь запущен")
    await client.send_voice("1203510398100447243", audio_path=r"C:\Users\as280\Pictures\minecraft\soundPad\nyaa-фара.mp3")

    # JSON данные для создания активности
    json_data = {
        'id': 'ed52e7003b57bc8',
        'created_at': 1723184107714,
        'name': 'и гладит фенька',
        'type': ActivityType.WATCHING,
        'assets':{
            'large_image': 'mp:attachments/1160759712900468839/1272141863276515378/trickmint.gif?ex=66b9e5ef&is=66b8946f&hm=3f093d3ec6bf5ea6ad68f1a20142832c27858672b5c126a2fc48174fea0e564a&'
        },
        "timestamps": {
            "start": int(datetime.datetime.now().timestamp())
        },
    }

    # Создание объекта Activity
    activity = Activity.from_json(json_data)

    # Установка активности пользователя
    await client.change_activity(activity=activity, status=PresenceStatus.ONLINE)

    # await client.change_activity(activity=CustomStatus(state="Охота на Peely!", end=0), status="online")
    # await client.change_activity(activity=NoActivity(), status="online")

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(client.start_polling())
