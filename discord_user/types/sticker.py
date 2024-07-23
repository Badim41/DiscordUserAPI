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
        """
        self.type = json_data['type']
        self.tags = json_data['tags']
        self.name = json_data['name']
        self.id = json_data['id']
        self.guild_id = json_data['guild_id']
        self.format_type = json_data['format_type']
        self.description = json_data['description']
        self.available = json_data['available']
        self.asset = json_data['asset']