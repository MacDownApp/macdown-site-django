import re
from django.http import HttpResponsePermanentRedirect
from django.conf import settings


class SecureRequiredMiddleware(object):
    """Forces HTTPS access for paths specified.
    """
    def __init__(self):
        try:
            pattern = settings.SECURE_REQUIRED_PATH_PATTERN
        except AttributeError:
            self.path_regex = None
        else:
            self.path_regex = re.compile(pattern)

    def process_request(self, request):
        if self.path_regex is None:
            return
        full_path = request.get_full_path()
        if not request.is_secure() and self.path_regex.match(full_path):
            request_url = request.build_absolute_uri()
            secure_url = request_url.replace('http://', 'https://')
            return HttpResponsePermanentRedirect(secure_url)
        return None
