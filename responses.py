def ApiResponse(message, data, status_code):
    return {
        "message": message,
        "data": data,
        "status_code": status_code
    }, status_code

def GetResponse(message, data, size, status_code):
    return {
        "message": message,
        "data": data,
        "size": size,
        "status_code": status_code
    }, status_code