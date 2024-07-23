import datetime


class Activity:
    """
    {
      "id": "d11307d8c0abb136",
      "created_at": "1695164784863",
      "details": "24H RL Stream for Charity",
      "state": "Rocket League",
      "name": "Twitch",
      "type": 1,
      "url": "https://www.twitch.tv/discord",
      "assets": {
        "large_image": "twitch:discord"
      }
    }


    {
      "id": "d11307d8c0abb135",
      "name": "Rocket League",
      "type": 0,
      "created_at": "1695164784863",
      "session_id": "30f32c5d54ae86130fc4a215c7474263",
      "application_id": "379286085710381999",
      "state": "In a Match",
      "details": "Ranked Duos: 2-1",
      "platform": "xbox",
      "flags": 0,
      "timestamps": {
        "start": "1695164482423"
      },
      "party": {
        "id": "9dd6594e-81b3-49f6-a6b5-a679e6a060d3",
        "size": [2, 2]
      },
      "assets": {
        "large_image": "351371005538729000",
        "large_text": "DFH Stadium",
        "small_image": "351371005538729111",
        "small_text": "Silver III"
      },
      "secrets": {
        "join": "025ed05c71f639de8bfaa0d679d7c94b2fdce12f"
      }
    }
    """

    """
    Пример:
    
    """
    def __init__(self, id, details, state, name, type:int, url, assets, created_at=datetime.datetime.now()):
        self.id = id
        self.created_at = created_at
        self.details = details
        self.state = state
        self.name = name
        self.type = type
        self.url = url
        self.assets = assets
    @staticmethod
    def from_json(json_data):
        type = json_data.get('type')
        state = json_data.get('state')
        name = json_data.get('name')
        id = json_data.get('id')
        created_at = json_data.get('created_at')
        details = json_data.get('details')
        url = json_data.get('url')
        assets = json_data.get('assets')
        return Activity(id=id, details=details, state=state, name=name, type=type, url=url, assets=assets, created_at=created_at)

    def to_dict(self):
        data = {}
        if self.id is not None:
            data['id'] = self.id
        if self.created_at is not None:
            data['created_at'] = self.created_at
        if self.details is not None:
            data['details'] = self.details
        if self.state is not None:
            data['state'] = self.state
        if self.name is not None:
            data['name'] = self.name
        if self.type is not None:
            data['type'] = self.type
        if self.url is not None:
            data['url'] = self.url
        if self.assets is not None:
            data['assets'] = self.assets
        return data


class ActivityType:
    # Играет {name}
    # пример: "Играет в Rocket League"
    PLAYING = 0

    # Стримит {details}
    # пример: "Стримит Rocket League"
    STREAMING = 1

    # Слушает {name}
    # пример: "Слушает Spotify"
    LISTENING = 2

    # Смотрит {name}
    # пример: "Смотрит YouTube Together"
    WATCHING = 3

    # Пользовательский {emoji} {state}
    # пример: "😃 I am cool"
    CUSTOM = 4

    # Соревнуется в {name}
    # пример: "Соревнуется в Arena World Champions"
    COMPETING = 5

    # Зависает {state} или {emoji} {details}
    # пример: "Chilling"
    HANG = 6

# activity = Activity()