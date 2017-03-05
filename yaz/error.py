class Error(Exception):
    def __init__(self, message, return_code: int = 1):
        super().__init__(message)
        self.return_code = return_code
