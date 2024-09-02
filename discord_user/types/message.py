from .user import User


class DiscordMessage:
    def __init__(self, data):
        self.type = data.get('type')
        self.tts = data.get('tts')
        self.timestamp = data.get('timestamp')
        self.referenced_message = None
        self.pinned = data.get('pinned')
        self.nonce = data.get('nonce')
        self.mentions = data.get('mentions')
        self.mention_roles = data.get('mention_roles')
        self.mention_everyone = data.get('mention_everyone')
        self.text = data['content']
        self.message_id = data['id']
        self.guild_id = data.get('guild_id', None)
        self.channel_id = data['channel_id']
        self.author = User(data['author'])
        self.attachments = data.get('attachments', [])
        self.sticker_items = data.get('sticker_items', [])
        self.embeds = data.get('embeds', [])
        self.components = data.get('components', [])
        self.edited_timestamp = data.get('edited_timestamp', None)

        if data.get('referenced_message'):
            self.referenced_message = DiscordMessage(data['referenced_message'])

    def __str__(self):
        return f"DiscordMessage(text={self.text}, message_id={self.message_id}, guild_id={self.guild_id}, channel_id={self.channel_id}, author={self.author}, attachments={self.attachments})"

    def to_dict(self):
        data = {
            'type': self.type,
            'tts': self.tts,
            'timestamp': self.timestamp,
            'referenced_message': self.referenced_message.to_dict() if self.referenced_message else None,
            'pinned': self.pinned,
            'nonce': self.nonce,
            'mentions': self.mentions,
            'mention_roles': self.mention_roles,
            'mention_everyone': self.mention_everyone,
            'content': self.text,
            'id': self.message_id,
            'guild_id': self.guild_id,
            'channel_id': self.channel_id,
            'author': self.author.to_dict() if self.author else None,
            'attachments': self.attachments,
            'sticker_items': self.sticker_items,
            'embeds': self.embeds,
            'components': self.components,
            'edited_timestamp': self.edited_timestamp
        }
        return data