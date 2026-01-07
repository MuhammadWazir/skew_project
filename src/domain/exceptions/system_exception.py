class SystemException(Exception):
    """
    Represents unexpected technical failures.

    Examples:
    - DB connection failure
    - OpenAI timeout
    - Vector DB unavailable
    """

    def __init__(
        self,
        message: str = "Internal system error",
        *,
        original_exception: Exception | None = None,
        service: str | None = None
    ):
        self.message = message
        self.original_exception = original_exception
        self.service = service

        super().__init__(message)
