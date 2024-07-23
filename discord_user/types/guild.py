from .channel import create_channel_from_json
from .emoji import Emoji
from .role import Role
from .sticker import Sticker


class Guild:
    def __init__(self, json_data):
        self.version = json_data['version']  # вообще не знаю что это
        self.threads = json_data['threads']  # TODO CLASS
        self.stickers = [Sticker(sticker_data) for sticker_data in json_data['stickers']]
        self.roles = [Role(role_data) for role_data in json_data['roles']]
        properties = json_data['properties']
        self.properties = properties
        self.verification_level = properties['verification_level']
        self.features = properties['features']
        self.name = properties['name']
        self.banner = properties['banner']
        self.rules_channel_id = properties['rules_channel_id']
        self.afk_channel_id = properties['afk_channel_id']
        self.description = properties['description']
        self.premium_tier = properties['premium_tier']  # Уровень буста Nitro
        self.clan = properties['clan']
        self.owner_id = properties['owner_id']
        self.system_channel_id = properties['system_channel_id']
        self.safety_alerts_channel_id = properties['safety_alerts_channel_id']
        self.icon = properties['icon']
        self.preferred_locale = properties['preferred_locale']
        self.member_count = json_data['member_count']
        self.lazy = json_data['lazy']  # не знаю что это
        self.large = json_data['large']
        self.joined_at = json_data['joined_at']
        self.id = json_data['id']
        self.guild_scheduled_events = json_data['guild_scheduled_events']
        self.emojis = [Emoji(emoji_data) for emoji_data in json_data['emojis']]
        self.channels = [create_channel_from_json(channel_data) for channel_data in json_data['channels']]
