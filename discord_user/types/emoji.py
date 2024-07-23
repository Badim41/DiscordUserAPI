class Emoji:
    def __init__(self, json_data):
        self.roles = json_data['roles']  # ???
        self.require_colons = json_data['require_colons']  # ???
        self.name = json_data['name']
        self.managed = json_data['managed']
        self.id = json_data['id']
        self.available = json_data['available']
        self.animated = json_data['animated']
