class BaseException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


NotFoundException = BaseException

ServicesNotFoundException = NotFoundException("Services not found.")

NotEmptyException = BaseException("Should be empty.")
