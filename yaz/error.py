__all__ = ["Error"]

class Error(Exception):
    """Can be thrown from within a yaz.task

    In contrast to other exceptions, throwing this Error class will
    not cause the call stack to be printed.  Instead, only the
    error message is printed to stdout.
    """

    def __init__(self, message, return_code: int = 1):
        super().__init__(message)
        self.return_code = return_code
