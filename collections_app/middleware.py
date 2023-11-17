#collections_app/middleware.py
import threading

class RequestCountMiddleware:
    _request_count = 0
    _lock = threading.Lock()

    @classmethod
    def _increment_request_count(cls):
        with cls._lock:
            cls._request_count += 1

    @classmethod
    def get_request_count(cls):
        with cls._lock:
            return cls._request_count

    @classmethod
    def reset_request_count(cls):
        with cls._lock:
            cls._request_count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self._increment_request_count()

        response = self.get_response(request)
        return response