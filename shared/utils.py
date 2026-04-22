from datetime import datetime
from typing import Any, Optional
import re

def sanitize_html(html: str) -> str:
    """Basic HTML sanitization - remove script tags."""
    return re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', html)

def format_timestamp(dt: Optional[datetime] = None) -> str:
    """Format datetime to ISO string."""
    if dt is None:
        dt = datetime.now()
    return dt.isoformat()

def validate_id(id: str) -> bool:
    """Validate document ID format."""
    return bool(re.match(r'^[a-zA-Z0-9_-]+$', id))

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to max length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def safe_get(data: dict, key: str, default: Any = None) -> Any:
    """Safely get value from dict."""
    return data.get(key, default)

class Result:
    """Result type for operations that can fail."""
    
    def __init__(self, success: bool, data: Any = None, error: str = None):
        self.success = success
        self.data = data
        self.error = error
    
    @classmethod
    def ok(cls, data: Any = None):
        return cls(True, data)
    
    @classmethod
    def fail(cls, error: str):
        return cls(False, None, error)
    
    def map(self, fn):
        """Map the data if success."""
        if self.success:
            return Result.ok(fn(self.data))
        return self