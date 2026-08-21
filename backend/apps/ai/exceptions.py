class AIError(Exception):
    """Base exception for all AI service errors."""
    pass

class AIConfigurationError(AIError):
    """Raised when the AI service is misconfigured."""
    pass

class AIAuthenticationError(AIError):
    """Raised when authentication with the AI provider fails."""
    pass

class AIRateLimitError(AIError):
    """Raised when the AI provider returns a rate limit error."""
    pass

class AITimeoutError(AIError):
    """Raised when the AI provider request times out."""
    pass

class AIServiceUnavailableError(AIError):
    """Raised when the AI provider is unavailable."""
    pass

class AIResponseError(AIError):
    """Raised when the AI response cannot be parsed or validated."""
    pass
