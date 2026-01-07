class CustomException(Exception):
    def __init__(self, status_code: int, data):
        self.status_code = status_code
        self.data = data
