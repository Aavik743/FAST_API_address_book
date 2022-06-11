class CustomException(Exception):
    def __init__(self, msg, code):
        self.Error = msg
        self.code = code


class NotFoundException(CustomException):
    pass


class NotMatchingException(CustomException):
    pass


class NotUniqueException(CustomException):
    pass


class InternalServerException(CustomException):
    pass
