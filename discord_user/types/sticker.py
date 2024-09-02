class Sticker:
    def __init__(self, json_data):
        """
        {
          'type': 2,
          'tags': 'sunglasses',
          'name': 'DimAss',
          'id': '862026969805094942',
          'guild_id': '345655283017842689',
          'format_type': 1,
          'description': None,
          'available': True,
          'asset': ''
        }

        {'name': 'Sup', 'id': '816087792291282944', 'format_type': 3}
        """
        self.name = json_data['name']
        self.id = json_data['id']
        self.format_type = json_data['format_type']

        self.type = json_data.get('type')
        self.tags = json_data.get('tags')
        self.guild_id = json_data.get('guild_id')
        self.description = json_data.get('description')
        self.available = json_data.get('available')
        self.asset = json_data.get('asset')
