# accounts/middleware/logging_middleware.py
from datetime import datetime
from django.utils.deprecation import MiddlewareMixin

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = request.META.get('REMOTE_ADDR')
        filename = f"{request.user.username if request.user.is_authenticated else ip}.log"
        method = request.method
        url = request.path
        start_time = datetime.now()
        log_message = f"[{start_time}] Request: Method={method}, URL={url}, IP={ip}\n"
        self.write_log(filename, log_message)
        request.start_time = start_time

    def process_response(self, request, response):
        end_time = datetime.now()
        ip = request.META.get('REMOTE_ADDR')
        filename = f"{request.user.username if request.user.is_authenticated else ip}.log"
        duration = end_time - request.start_time
        log_message = f"[{end_time}] Response: Status={response.status_code}, Duration={duration.total_seconds()} seconds\n"
        self.write_log(filename, log_message)
        return response

    def write_log(self, filename, message):
        with open(filename, "a", encoding="utf-8") as log_file:
            log_file.write(message)
