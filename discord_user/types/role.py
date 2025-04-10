class Role:
    def __init__(self, json_data):
        """
        {
          'unicode_emoji': None,
          'tags': {},
          'position': 3,
          'permissions_new': '0',
          'permissions': 0,
          'name': 'Игрок',
          'mentionable': False,
          'managed': False,
          'id': '1139520863847333999',
          'icon': None,
          'hoist': False,
          'flags': 1,
          'color': 0
        }
        """
        self.unicode_emoji = json_data.get('unicode_emoji')
        self.tags = json_data.get('tags')
        """
        'tags': {
            'bot_id': '559426966151757824'
            'integration_id': '937790974703308820'
          }
        """
        self.position = json_data.get('position')
        # self.permissions_new = json_data.get('permissions_new')
        self.permissions = json_data.get('permissions')
        self.name = json_data.get('name')
        self.mentionable = json_data.get('mentionable')
        self.managed = json_data.get('managed')  # не знаю что это
        self.id = json_data.get('id')
        self.icon = json_data.get('icon')
        self.hoist = json_data.get('hoist')  # не знаю что это
        self.flags = json_data.get('flags')
        self.color = json_data.get('color')
