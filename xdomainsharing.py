from django import http
from django.conf import settings
from django.utils.text import compress_string
from django.utils.cache import patch_vary_headers


class CrossDomainSharingMiddleware(object):
    """
    Middleware to allow cross-domain XHR requests in django

    Access-Control-Allow-Origin: http://domain.example
    Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE
    """
    def __init__(self):
        self.CROSS_DOMAIN_ALLOWED_ORIGINS = getattr(
            settings,
            'CROSS_DOMAIN_ALLOWED_ORIGINS', 
            '*'
        )

        self.CROSS_DOMAIN_ALLOWED_METHODS = getattr(
            settings,
            'CROSS_DOMAIN_ALLOWED_METHODS',
            ['POST','GET','OPTIONS', 'PUT', 'DELETE']
        )

    def process_request(self, request):
        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()

            response['Access-Control-Allow-Origin']  = \
                self.CROSS_DOMAIN_ALLOWED_ORIGINS
            response['Access-Control-Allow-Methods'] = \
                ",".join(self.CROSS_DOMAIN_ALLOWED_METHODS)

            return response

        return None

    def process_response(self, request, response):
        # Avoid unnecessary work
        if response.has_header('Access-Control-Allow-Origin'):
            return response

        response['Access-Control-Allow-Origin'] = \
            self.CROSS_DOMAIN_ALLOWED_ORIGINS
        response['Access-Control-Allow-Methods'] = \
            ",".join(self.CROSS_DOMAIN_ALLOWED_METHODS)

        return response
