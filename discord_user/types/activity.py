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

    {"name": "Custom Status", "type": 4, "state": "хых", "timestamps": {"end": 1723204799999}, "emoji": null}
    """

    """
    Пример:
    
    """

    def __init__(self, state: str, name: str, type: int, id=None, details=None, url=None, assets=None, created_at=None,
                 timestamps=None, secrets=None, emoji=None, session_id=None, application_id=None, platform=None,
                 party=None, metadata=None, buttons=None):
        self.id = id
        self.created_at = created_at
        self.details = details
        self.state = state
        self.name = name
        self.type = type
        self.url = url
        self.assets = assets
        self.timestamps = timestamps
        self.secrets = secrets
        self.emoji = emoji
        self.session_id = session_id
        self.application_id = application_id
        self.platform = platform
        self.party = party
        self.metadata = metadata
        self.buttons = buttons

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
        secrets = json_data.get('secrets')
        timestamps = json_data.get('timestamps')
        emoji = json_data.get('emoji')
        session_id = json_data.get('session_id')
        application_id = json_data.get('application_id')
        platform = json_data.get('platform')
        party = json_data.get('party')
        metadata = json_data.get('metadata')
        buttons = json_data.get('buttons')

        return Activity(id=id, details=details, state=state, name=name, type=type, url=url, assets=assets,
                        created_at=created_at, secrets=secrets, timestamps=timestamps, emoji=emoji,
                        session_id=session_id, application_id=application_id, platform=platform, party=party,
                        metadata=metadata, buttons=buttons)

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
        if self.secrets is not None:
            data['secrets'] = self.secrets
        if self.timestamps is not None:
            data['timestamps'] = self.timestamps
        if self.emoji is not None:
            data['emoji'] = self.emoji
        if self.session_id is not None:
            data['session_id'] = self.session_id
        if self.application_id is not None:
            data['application_id'] = self.application_id
        if self.platform is not None:
            data['platform'] = self.platform
        if self.party is not None:
            data['party'] = self.party
        if self.metadata is not None:
            data['metadata'] = self.metadata
        if self.buttons is not None:
            data['buttons'] = self.buttons
        data["flags"] = 1

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


class CustomStatus(Activity):
    """
    {"name": "Custom Status", "type": 4, "state": "хых", "timestamps": {"end": 1723204799999}, "emoji": null}
    """

    def __init__(
            self,
            state: str,
            end: int = None,
            emoji: str = None,
    ):
        """
        state - текст статуса
        end - timestamp когда закончится
        """
        name = "Custom Status"
        type = 4

        if end:
            timestamps = {"end": end}
        else:
            timestamps = None

        details = None
        id = None
        url = None
        assets = None
        secrets = None
        created_at = None

        # Инициализируем Activity с помощью родительского конструктора
        super().__init__(id=id, details=details, state=state, name=name, type=type, url=url, assets=assets,
                         created_at=created_at, secrets=secrets, timestamps=timestamps, emoji=emoji)


class SimpleStatus(Activity):
    """
    {'type': 0, 'timestamps': {'start': 1723180000704}, 'name': 'Точно НЕ взламывает Пинтагон',
         'id': 'ed52e7003b57bc8', 'created_at': 1723180002204}
    """

    def __init__(
            self,
            name: str,
            id: str,
            type: int,
            start=int(datetime.datetime.now().timestamp()),
            details=None,
            url=None,
            assets=None,
            secrets=None,
            created_at=datetime.datetime.now(),
            state=None
    ):
        name = name
        id = id

        if start:
            timestamps = {"start": start}
        else:
            timestamps = None

        # Инициализируем Activity с помощью родительского конструктора
        super().__init__(id=id, details=details, state=state, name=name, type=type, url=url, assets=assets,
                         created_at=created_at, secrets=secrets, timestamps=timestamps)


class NoActivity(Activity):
    def __init__(self):
        super().__init__(state="", name="", type=0)
        self.state = None
        self.name = None
        self.type = None

    def to_dict(self):
        return []
