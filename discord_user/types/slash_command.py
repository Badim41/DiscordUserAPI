import json

from .embed import Embed
from .interaction_metadata import InteractionMetadata
from .user import User
from ..utils.time_util import get_nonce

class SlashCommand:
    def __init__(self, type, application_id, guild_id, channel_id, session_id, data: dict, analytics_location, options=None):
        self.type = type
        self.application_id = application_id
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.session_id = session_id
        self.data = data
        self.analytics_location = analytics_location
        self.options = options

    def to_json(self):
        json_data = {
            "type": self.type,
            "application_id": self.application_id,
            "guild_id": self.guild_id,
            "channel_id": self.channel_id,
            "session_id": self.session_id,
            "data": self.data,
            "nonce": get_nonce()
        }

        if self.analytics_location:
            json_data['analytics_location'] = self.analytics_location
        if self.options:
            json_data['options'] = self.options

        return json.dumps(json_data)

    @classmethod
    def from_dict(cls, json_data, session_id):
        required_fields = ["type", "application_id", "guild_id", "channel_id", "data", "analytics_location"]
        for field in required_fields:
            if field not in json_data:
                raise ValueError(f"Missing required field: {field}")

        return cls(
            type=json_data["type"],
            application_id=json_data["application_id"],
            guild_id=json_data["guild_id"],
            channel_id=json_data["channel_id"],
            session_id=session_id,
            data=json_data["data"],
            analytics_location=json_data.get("analytics_location", None),
            options=json_data.get("options", None)
        )


class SlashCommandMessage:
    """
    {
  'webhook_id': '464272403766444044',
  'type': 0,
  'tts': False,
  'timestamp': '2024-07-22T01:50:01.868000+00:00',
  'position': 0,
  'pinned': False,
  'message_reference': {
    'type': 0,
    'message_id': '1264761337624662037',
    'guild_id': '1069196218447691836',
    'channel_id': '1070713643387330590'
  },
  'mentions': [],
  'mention_roles': [],
  'mention_everyone': False,
  'interaction_metadata': {
    'user': {
      'username': 'badim42',
      'public_flags': 4194304,
      'id': '544816254435983360',
      'global_name': 'badim42',
      'discriminator': '0',
      'clan': None,
      'avatar_decoration_data': None,
      'avatar': '581bf311aae5a97608d00b6c0f85d4b4'
    },
    'type': 2,
    'original_response_message_id': '1264761337624662037',
    'name': 'up',
    'id': '1264761336563503107',
    'authorizing_integration_owners': {
      '0': '1069196218447691836'
    }
  },
  'id': '1264761341185495093',
  'flags': 64,
  'embeds': [
    {
      'type': 'rich',
      'image': {
        'width': 300,
        'url': 'https://cdn.discordapp.com/ephemeral-attachments/1070713643387330590/1264761341252735038/code.jpeg?ex=669f0c49&is=669dbac9&hm=18baad6418c5906ea1a697337c815bced63c3ece7e1a93be61a6668078f3e43f&',
        'proxy_url': 'https://media.discordapp.net/ephemeral-attachments/1070713643387330590/1264761341252735038/code.jpeg?ex=669f0c49&is=669dbac9&hm=18baad6418c5906ea1a697337c815bced63c3ece7e1a93be61a6668078f3e43f&',
        'height': 80
      },
      'footer': {
        'text': 'Срок действия кода: 15 секунд'
      },
      'description': 'Введите число, написанное на изображении, используя команду `/up XXXX`',
      'content_scan_version': 0,
      'color': 7506394,
      'author': {
        'url': 'https://server-discord.com/1069196218447691836',
        'proxy_icon_url': 'https://images-ext-1.discordapp.net/external/ADCFB1oOtztcw6Q07H1MEjqbo1Un8XA9j_VqGR5izHI/https/cdn.discordapp.com/icons/1069196218447691836/ba062888b35557bc0754223e70e6a7d0.webp',
        'name': 'Mijue',
        'icon_url': 'https://cdn.discordapp.com/icons/1069196218447691836/ba062888b35557bc0754223e70e6a7d0.webp'
      }
    }
  ],
  'edited_timestamp': None,
  'content': '',
  'components': [],
  'channel_id': '1070713643387330590',
  'author': {
    'username': 'SD.C Monitoring',
    'public_flags': 65536,
    'id': '464272403766444044',
    'global_name': None,
    'discriminator': '9896',
    'clan': None,
    'bot': True,
    'avatar_decoration_data': None,
    'avatar': '64d9bd50cf329f80d3d66b9aab000f8e'
  },
  'attachments': [],
  'application_id': '464272403766444044'
}
    """

    def __init__(self, json_data):
        from ..client import _log
        _log.info(f"slash data: {json_data}")
        self.webhook_id = json_data.get('webhook_id')
        self.type = json_data.get('type')
        self.tts = json_data.get('tts')
        self.timestamp = json_data.get('timestamp')
        self.position = json_data.get('position')
        self.pinned = json_data.get('pinned')
        self.message_reference = json_data.get('message_reference', {})
        self.mentions = json_data.get('mentions', [])
        self.mention_roles = json_data.get('mention_roles', [])
        self.mention_everyone = json_data.get('mention_everyone')
        self.interaction_metadata = InteractionMetadata(json_data.get('interaction_metadata', {}))
        self.id = json_data.get('id')
        self.flags = json_data.get('flags')
        self.embeds = [Embed(embed) for embed in json_data.get('embeds', [])]
        self.edited_timestamp = json_data.get('edited_timestamp')
        self.content = json_data.get('content')
        self.components = json_data.get('components', [])
        self.channel_id = json_data.get('channel_id')
        self.author = User(json_data.get('author', {}))
        self.attachments = json_data.get('attachments', [])
        self.application_id = json_data.get('application_id')

    def __repr__(self):
        return f"<SlashCommandMessage id={self.id} author={self.author.username} content={self.content}>"

# class SlashCommandType:
#     IN_PROCESS = 0
#     COMPLETED = 2
