"""
LooLu is Copyright (c) 2009 Shannon Johnson, http://loo.lu/

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import re, logging

from urlparse import urlparse
from django.conf import settings

from model import PageRequest


class LogRequestMiddleware(object):
    def process_request(self, request):
        setattr(request, 'logrequest', getattr(
                settings, 'LOG_REQUEST_ALL', True))

        return None

    def process_response(self, request, response):
        if not hasattr(request, 'logrequest') or not request.logrequest:
            return response

        referrer_host = None
        referrer_uri  = None
        referrer      = request.META.get('HTTP_REFERER') 
 
        if referrer:
            (p, referrer_host, referrer_uri, d, q, f) = urlparse(
                referrer, 'http')
            if q: referrer_uri += '?' + q

        """
        Django does not actually commit a session to the backend 
        cache/db/file and set the cookie header *unless* the     
        the session object has been modified
        """
        session_key = None
        if hasattr(request, 'session'):
            if request.session.modified or settings.SESSION_SAVE_EVERY_REQUEST:
                session_key = request.session.session_key
            else:
                session_key = request.COOKIES.get(
                    settings.SESSION_COOKIE_NAME, None)

        log = PageRequest(
                  method         = request.META.get('REQUEST_METHOD'),
                  secure         = request.is_secure(),
                  host           = request.get_host(), 
                  file           = request.path,
                  query_string   = request.META.get('QUERY_STRING'),
                  status_code    = response.status_code, 
                  ip             = request.META.get('REMOTE_ADDR'),
                  user_agent     = request.META.get('HTTP_USER_AGENT'),
                  accept_lang    = request.META.get('HTTP_ACCEPT_LANGUAGE'),
                  referrer_host  = referrer_host,
                  referrer_uri   = referrer_uri,
                  session_key    = session_key)

        try:
            log.put()
        except:
            logging.error(traceback.format_exc())

        return response
