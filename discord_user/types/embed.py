class EmbedImage:
    def __init__(self, json_data):
        self.width = json_data.get('width')
        self.url = json_data.get('url')
        self.proxy_url = json_data.get('proxy_url')
        self.height = json_data.get('height')

class EmbedFooter:
    def __init__(self, json_data):
        self.text = json_data.get('text')

class EmbedAuthor:
    def __init__(self, json_data):
        self.url = json_data.get('url')
        self.proxy_icon_url = json_data.get('proxy_icon_url')
        self.name = json_data.get('name')
        self.icon_url = json_data.get('icon_url')

class Embed:
    def __init__(self, json_data):
        self.type = json_data.get('type')
        self.image = EmbedImage(json_data.get('image', {}))
        self.footer = EmbedFooter(json_data.get('footer', {}))
        self.description = json_data.get('description')
        self.content_scan_version = json_data.get('content_scan_version')
        self.color = json_data.get('color')
        self.author = EmbedAuthor(json_data.get('author', {}))