def ApiResponse(message, data, status_code):
    return {
        "message": message,
        "data": data,
        "status_code": status_code
    }, status_code