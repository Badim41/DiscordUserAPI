from typing import List

from .guild import Guild


class User:
    def __init__(self, json_data):
        # print("USER DATA:", json_data)
        self.username: str = json_data.get("username", None)
        self.id: str = json_data.get("id", None)
        self.public_flags: int = json_data.get("public_flags", 0)
        self.global_name: str = json_data.get("global_name", None) or json_data.get("display_name", None)
        self.discriminator: str = json_data.get("discriminator", None)  # тэг, например #0001
        self.clan = json_data.get("clan", None)
        self.avatar_decoration_data = json_data.get("avatar_decoration_data", None)
        self.avatar: str = json_data.get("avatar", None)
        self.bot: bool = json_data.get("bot", None)# не 100% вариант

    def __str__(self):
        return f"DiscordAuthor(username={self.username}, id={self.id}, avatar={self.avatar}, global_name={self.global_name}, discriminator={self.discriminator}, clan={self.clan}, avatar_decoration_data={self.avatar_decoration_data})"


class SelfUserInfo:
    def __init__(self, json_data):
        with open("user_info.json", "w", encoding="utf-8") as writer:
            writer.write(str(json_data))
        self.local_message_users = {user_data['id']: User(user_data) for user_data in json_data['users']}
        self.user_guild_settings = json_data['user_guild_settings']
        self_user = json_data['user']
        self.is_verified: bool = self_user['verified']
        self.username: str = self_user['username']
        self.is_nitro: bool = self_user['premium']
        self.phone: str = self_user['phone']
        self.email: str = self_user['email']
        self.global_name: str = self_user['global_name']
        self.relationships = json_data['relationships']
        self.friends_id: List[str] = []

        for relationship_data in self.relationships:
            if relationship_data['type'] == 1:
                self.friends_id.append(relationship_data['id'])

        self.merged_members = json_data['merged_members']
        """
        'merged_members': [
            [
              {
                'user_id': '820845312217317397',
                'roles': [
                  '426392810456088596'
                ],
                'premium_since': None,
                'pending': False,
                'nick': None,
                'mute': False,
                'joined_at': '2023-08-24T05:34:58.958000+00:00',
                'flags': 10,
                'deaf': False,
                'communication_disabled_until': None,
                'banner': None,
                'avatar': None
              }
            ],
            
            ...
            
        ]
        """
        self.guilds = {guild_data['id']: Guild(guild_data) for guild_data in json_data['guilds']}
        self.regions: List[str] = json_data['geo_ordered_rtc_regions']
        self.session_id = json_data['session_id']