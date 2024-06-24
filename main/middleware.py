from django.utils.deprecation import MiddlewareMixin


# overriding the default middleware implementation
# to make sure pages are not cached.
# This is a less data-centric application and removing
# cache and revalidating the user, prevents unauthorized
# access to teh webpages by not allowing access via 'back'
# 'forward' button on browser.
class NoCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
        return response
