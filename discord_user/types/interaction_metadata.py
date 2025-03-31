class InteractionMetadata:
    def __init__(self, json_data):
        from ..types import User
        self._data = json_data
        self.user = User(json_data.get('user', {}))
        self.type = json_data.get('type')
        self.original_response_message_id = json_data.get('original_response_message_id')
        self.name = json_data.get('name')
        self.id = json_data.get('id')
        self.authorizing_integration_owners = json_data.get('authorizing_integration_owners', {})
