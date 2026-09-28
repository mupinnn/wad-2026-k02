from typing import Any


def success_response(message: str, data: Any = None):
    return {
        "status": "success",
        "message": message,
        "data": data
    }


def error_response(message: str, data: Any = None):
    return {
        "status": "error",
        "message": message,
        "data": data
    }