class APIError(Exception):
    def __init__(self, status_code, payload):
        super().__init__(self)
        self.status_code = status_code
        self.payload = payload
