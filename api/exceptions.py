class APIError(Exception):
    """基礎 API 錯誤類"""
    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.status_code = status_code

class DifyAPIError(APIError):
    """Dify API 相關錯誤"""
    pass

class GoogleMapsAPIError(APIError):
    """Google Maps API 相關錯誤"""
    pass

class ValidationError(APIError):
    """輸入驗證錯誤"""
    def __init__(self, message):
        super().__init__(message, status_code=400) 