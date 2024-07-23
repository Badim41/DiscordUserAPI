from discord_user.types import User, Activity


class PresenceStatus:
    ONLINE = "online"  # Онлайн
    IDLE = "idle"  # Неактивен
    DND = "dnd"  # Не беспокоить
    INVISIBLE = "invisible"  # невидимый

class Game:
    def __init__(self, json_data):
        # print("game:", json_data)
        self.type = json_data.get('type', None)
        self.state = json_data.get('state', None)
        self.session_id = json_data.get('session_id', None)
        self.name = json_data.get('name', None)
        self.id = json_data.get('id', None)
        self.created_at = json_data.get('created_at', None)

class Presence:
    def __init__(self, json_data):
        # print("presence", json_data)
        """
        # bot presence
        {
          'user': {
            'id': '310848622642069504'
          },
          'status': 'idle',
          'roles': [
            '1139159900207976451',
            '1069278375618805853'
          ],
          'premium_since': None,
          'nick': None,
          'guild_id': '1069196218447691836',
          'game': {
            'type': 4,
            'state': 'https://juniper.bot',
            'session_id': None,
            'name': 'Custom Status',
            'id': 'ec0b28a579ecb4bd',
            'created_at': 1721293245972
          },
          'client_status': {
            'web': 'idle'
          },
          'broadcast': None,
          'activities': [
            {
              'type': 4,
              'state': 'https://juniper.bot',
              'name': 'Custom Status',
              'id': 'ec0b28a579ecb4bd',
              'created_at': 1721293245972
            }
          ]
        }

        # User presence
        {
          'user': {
            'username': 'badim42',
            'public_flags': 4194304,
            'id': '544816254435983360',
            'global_name': 'badim42',
            'discriminator': '0',
            'clan': None,
            'avatar_decoration_data': None,
            'avatar': 'cc909d956b8538bda4df5ef7c7f5fba6'
          },
          'status': 'idle',
          'last_modified': 1721292997666,
          'client_status': {
            'web': 'idle',
            'desktop': 'idle'
          },
          'activities': [
            {
              'type': 0,
              'timestamps': {
                'start': 1721292413026
              },
              'name': 'main.py – discord_bot.py',
              'id': '70004536a4e87f32',
              'created_at': 1721292413731
            }
          ]
        }
        """
        self.user = User(json_data.get('user'))
        self.is_on_guild = self.user.username
        self.status = json_data.get('status')
        self.role_ids = json_data.get('roles', [])
        self.premium_since = json_data.get('premium_since')
        self.nick = json_data.get('nick')
        self.guild_id = json_data.get('guild_id')
        game = json_data.get('game', {})
        if game:
            self.game = Game(game)

        self.client_status = json_data.get('client_status', {})
        self.broadcast = json_data.get('broadcast')
        self.activities = [Activity.from_json(activity) for activity in json_data.get('activities', [])]
        self.last_modified = json_data.get('last_modified')