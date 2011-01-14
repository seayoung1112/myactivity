from django.conf import settings
from django.http import HttpResponseServerError

import traceback

class AJAXSimpleExceptionResponse:
    def process_exception(self, request, exception):
        if settings.DEBUG and request.is_ajax():
                traceback.print_exc()
