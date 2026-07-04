"""Custom exceptions for the application."""

from typing import Dict, List, Optional


class ApplicationError(Exception):
    """Base application error."""

    def __init__(
        self,
        code: str,
        message: str,
        details: Optional[List[Dict]] = None,
        status_code: int = 400,
    ):
        """Initialize error."""
        self.code = code
        self.message = message
        self.details = details or []
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(ApplicationError):
    """Validation error."""

    def __init__(self, message: str, details: Optional[List[Dict]] = None):
        """Initialize validation error."""
        super().__init__("INVALID_INPUT", message, details, 400)


class UnauthorizedError(ApplicationError):
    """Unauthorized error."""

    def __init__(self, message: str = "Invalid credentials"):
        """Initialize unauthorized error."""
        super().__init__("UNAUTHORIZED", message, status_code=401)


class ForbiddenError(ApplicationError):
    """Forbidden error."""

    def __init__(self, message: str = "Access denied"):
        """Initialize forbidden error."""
        super().__init__("FORBIDDEN", message, status_code=403)


class NotFoundError(ApplicationError):
    """Not found error."""

    def __init__(self, message: str = "Resource not found"):
        """Initialize not found error."""
        super().__init__("NOT_FOUND", message, status_code=404)


class ConflictError(ApplicationError):
    """Conflict error."""

    def __init__(self, message: str):
        """Initialize conflict error."""
        super().__init__("CONFLICT", message, status_code=409)


class DuplicateResourceError(ApplicationError):
    """Duplicate resource error."""

    def __init__(self, message: str = "Resource already exists"):
        """Initialize duplicate resource error."""
        super().__init__("DUPLICATE_RESOURCE", message, status_code=400)


class UnprocessableError(ApplicationError):
    """Unprocessable entity error."""

    def __init__(self, message: str, details: Optional[List[Dict]] = None):
        """Initialize unprocessable error."""
        super().__init__("UNPROCESSABLE", message, details, 422)


class RateLimitError(ApplicationError):
    """Rate limit error."""

    def __init__(self, message: str = "Too many requests"):
        """Initialize rate limit error."""
        super().__init__("RATE_LIMIT", message, status_code=429)


class DependencyUnavailableError(ApplicationError):
    """Dependency unavailable error."""

    def __init__(self, message: str = "Required service or database unavailable"):
        """Initialize dependency unavailable error."""
        super().__init__("DEPENDENCY_UNAVAILABLE", message, status_code=503)
