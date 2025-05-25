class DataValidationError(Exception):
    """Raised when input data fails schema or sanity checks."""
    def __init__(self, message: str):
        super().__init__(message)
