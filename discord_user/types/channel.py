
class Channel:
    """
            VOICE CHAT
            {
              'user_limit': 0,
              'type': 2,
              'status': None,
              'rtc_region': None,
              'rate_limit_per_user': 0,
              'position': 0,
              'permission_overwrites': [
                {
                  'type': 'role',
                  'id': '1170244843302309908',
                  'deny_new': '0',
                  'deny': 0,
                  'allow_new': '1049600',
                  'allow': 1049600
                },
                {
                  'type': 'role',
                  'id': '1056451533623021578',
                  'deny_new': '1049600',
                  'deny': 1049600,
                  'allow_new': '0',
                  'allow': 0
                }
              ],
              'parent_id': '1056451533623021580',
              'name': 'Приватный',
              'last_message_id': '1201465577563246634',
              'id': '1056451533623021582',
              'icon_emoji': {
                'name': '🔒',
                'id': None
              },
              'flags': 0,
              'bitrate': 64000
            },


            TEXT CHAT
            {
              'type': 0,
              'topic': 'Смотри в закрепе!\n/say\n/read_messages',
              'rate_limit_per_user': 5,
              'position': 12,
              'permission_overwrites': [
                {
                  'type': 'role',
                  'id': '1173025056415289364',
                  'deny_new': '71314442432529',
                  'deny': 805449745,
                  'allow_new': '139586817088',
                  'allow': 379968
                },
                {
                  'type': 'role',
                  'id': '1056451533623021578',
                  'deny_new': '1024',
                  'deny': 1024,
                  'allow_new': '0',
                  'allow': 0
                }
              ],
              'parent_id': '1173044006985404426',
              'name': '🤖gpt',
              'last_pin_timestamp': '2023-11-11T22:25:30+00:00',
              'last_message_id': '1236787713097859132',
              'id': '1168343034589610067',
              'icon_emoji': {
                'name': '🤖',
                'id': None
              },
              'flags': 0
            },

            # FORUM
            {
              'type': 15,
              'topic': None,
              'template': '',
              'rate_limit_per_user': 60,
              'position': 8,
              'permission_overwrites': [
                {
                  'type': 'role',
                  'id': '1173025056415289364',
                  'deny_new': '70936485310481',
                  'deny': 805449745,
                  'allow_new': '414464724032',
                  'allow': 379968
                },
                {
                  'type': 'role',
                  'id': '1056451533623021578',
                  'deny_new': '3072',
                  'deny': 3072,
                  'allow_new': '0',
                  'allow': 0
                }
              ],
              'parent_id': '1056451533623021579',
              'name': '✨вопросы-и-предложения',
              'last_message_id': None,
              'id': '1173043622376112199',
              'icon_emoji': {
                'name': '🤔',
                'id': None
              },
              'flags': 16,
              'default_thread_rate_limit_per_user': 5,
              'default_sort_order': 1,
              'default_reaction_emoji': {
                'emoji_name': '⬆️',
                'emoji_id': None
              },
              'default_forum_layout': 1,
              'available_tags': [
                {
                  'name': 'Предложения',
                  'moderated': False,
                  'id': '1173044285998911499',
                  'emoji_name': None,
                  'emoji_id': None
                },
                {
                  'name': 'Баги',
                  'moderated': False,
                  'id': '1173044305867325450',
                  'emoji_name': None,
                  'emoji_id': None
                },
                {
                  'name': 'Вопросы',
                  'moderated': False,
                  'id': '1173044325135941722',
                  'emoji_name': None,
                  'emoji_id': None
                }
              ]
            },

            CATRGORY
            {
              'type': 4,
              'position': 0,
              'permission_overwrites': [],
              'name': 'заявки',
              'id': '1173055558790692904',
              'flags': 0
            },

            # STAGE
            {
              'user_limit': 10000,
              'type': 13,
              'topic': None,
              'rtc_region': None,
              'rate_limit_per_user': 0,
              'position': 8,
              'permission_overwrites': [
                {
                  'type': 'role',
                  'id': '1122876889313325086',
                  'deny_new': '0',
                  'deny': 0,
                  'allow_new': '20971536',
                  'allow': 20971536
                }
              ],
              'parent_id': '1122502360338538596',
              'nsfw': False,
              'name': 'no air',
              'last_message_id': '1222130017408909405',
              'id': '1222128886939123754',
              'flags': 0,
              'bitrate': 64000
            },
            """
    def __init__(self, json_data):
        self.id = json_data.get('id')
        self.name = json_data.get('name')
        self.type = json_data.get('type')
        self.position = json_data.get('position')
        self.permission_overwrites = json_data.get('permission_overwrites')
        self.parent_id = json_data.get('parent_id')
        self.flags = json_data.get('flags')
        self.last_message_id = json_data.get('last_message_id')
        self.icon_emoji = json_data.get('icon_emoji')


class TextChannel(Channel):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.topic = json_data.get('topic')
        self.rate_limit_per_user = json_data.get('rate_limit_per_user')
        self.last_pin_timestamp = json_data.get('last_pin_timestamp')


class VoiceChannel(Channel):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.bitrate = json_data.get('bitrate')
        self.user_limit = json_data.get('user_limit')
        self.rtc_region = json_data.get('rtc_region')
        self.rate_limit_per_user = json_data.get('rate_limit_per_user')


class NewsChannel(Channel):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.topic = json_data.get('topic')
        self.rate_limit_per_user = json_data.get('rate_limit_per_user')
        self.last_pin_timestamp = json_data.get('last_pin_timestamp')


class StageChannel(Channel):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.bitrate = json_data.get('bitrate')
        self.user_limit = json_data.get('user_limit')
        self.rtc_region = json_data.get('rtc_region')
        self.rate_limit_per_user = json_data.get('rate_limit_per_user')
        self.nsfw = json_data.get('nsfw')


class ForumChannel(Channel):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.topic = json_data.get('topic')
        self.template = json_data.get('template')
        self.rate_limit_per_user = json_data.get('rate_limit_per_user')
        self.default_thread_rate_limit_per_user = json_data.get('default_thread_rate_limit_per_user')
        self.default_sort_order = json_data.get('default_sort_order')
        self.default_reaction_emoji = json_data.get('default_reaction_emoji')
        self.default_forum_layout = json_data.get('default_forum_layout')
        self.available_tags = json_data.get('available_tags')
class ChannelType:
    TEXT = 0
    DM = 1 # не знаю
    VOICE = 2
    GROUP_DM = 3 # не знаю
    CATEGORY = 4
    NEWS = 5 # объявления
    STAGE = 13
    FORUM = 15

def create_channel_from_json(json_data):
    channel_type = json_data.get('type')
    if channel_type == ChannelType.TEXT:
        return TextChannel(json_data)
    elif channel_type == ChannelType.VOICE:
        return VoiceChannel(json_data)
    elif channel_type == ChannelType.NEWS:
        return NewsChannel(json_data)
    elif channel_type == ChannelType.STAGE:
        return StageChannel(json_data)
    elif channel_type == ChannelType.FORUM:
        return ForumChannel(json_data)
    else:
        return Channel(json_data)