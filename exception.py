class IncorrectCommand(BaseException):

    def __init__(self, message: str = "", cause: BaseException = None):
        super()
        self._cause = cause
        self._message = message

    def __str__(self) -> str:
        return f"{self._message}\n{self._cause}"
