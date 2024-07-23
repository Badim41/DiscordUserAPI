import discord_user
from discord_user.types.slash_command import SlashCommand

# Создание объекта SlashCommand из словаря
json_data_up_2 = {
    "type": 2,
    "application_id": "464272403766444044",
    "guild_id": "1069196218447691836",
    "channel_id": "1070713643387330590",
    "session_id": "cf126488b33eaed6e515f83e5cc74e15",
    "data": {
        "version": "891377101494681661",
        "id": "891377101494681660",
        "name": "up",
        "type": 1,
        "options": [{"type": 4, "name": "код", "value": 1231}],
        "application_command": {
            "id": "891377101494681660",
            "type": 1,
            "application_id": "464272403766444044",
            "version": "891377101494681661",
            "name": "up",
            "description": "Апнуть сервер",
            "options": [{"type": 4, "name": "код", "description": "Код капчи", "description_localized": "Код капчи",
                         "name_localized": "код"}],
            "integration_types": [0],
            "global_popularity_rank": 1,
            "description_localized": "Апнуть сервер",
            "name_localized": "up"
        },
        "attachments": []
    },
    "nonce": "1264406719774064640",
    "analytics_location": "slash_ui"
}

json_data_up_1 = {"type":2,"application_id":"464272403766444044","guild_id":"1069196218447691836","channel_id":"1070713643387330590","session_id":"fd8a4707dbaff895490bfcaf1fea7b9f","data":{"version":"891377101494681661","id":"891377101494681660","name":"up","type":1,"options":[],"application_command":{"id":"891377101494681660","type":1,"application_id":"464272403766444044","version":"891377101494681661","name":"up","description":"Апнуть сервер","options":[{"type":4,"name":"код","description":"Код капчи","description_localized":"Код капчи","name_localized":"код"}],"integration_types":[0],"global_popularity_rank":1,"description_localized":"Апнуть сервер","name_localized":"up"},"attachments":[]},"nonce":"1264535763899383808","analytics_location":"slash_ui"}

client: discord_user.Client = None  # заглушка

command = SlashCommand.from_dict(json_data_up_2, session_id="cf126488b33eaed6e515f83e5cc74e15")
print(json_data_up_2)
print(command.to_json())  # Выводит словарь, аналогичный json_data

