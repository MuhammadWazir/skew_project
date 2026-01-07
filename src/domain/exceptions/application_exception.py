class ApplicationException(Exception):
    """
    Represents an expected, business-level failure.

    Examples:
    - Invalid input
    - Entity not found
    - Operation not allowed
    """

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        details: dict | None = None
    ):
        self.message = message
        self.code = code
        self.details = details or {}

        super().__init__(message)
