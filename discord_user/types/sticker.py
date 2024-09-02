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

    def is_exportable(self):
        return self.format_type == 1

    def get_url(self):
        if self.is_exportable():
            return f"https://media.discordapp.net/stickers/{self.id}.webp?size=4096"
        else:
            return f"{self.name} ({self.id}) имеет формат {self.format_type}, который нельзя экспортировать ссылкой"

    def to_dict(self):
        return {
            'name': self.name,
            'id': self.id,
            'format_type': self.format_type,
            'type': self.type,
            'tags': self.tags,
            'guild_id': self.guild_id,
            'description': self.description,
            'available': self.available,
            'asset': self.asset
        }
