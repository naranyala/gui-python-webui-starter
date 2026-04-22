def format_response(success: bool, data: any = None, error: str = None):
    """Standard API response format."""
    return {
        "success": success,
        "data": data,
        "error": error
    }
