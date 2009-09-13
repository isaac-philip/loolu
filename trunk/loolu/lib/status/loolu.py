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

from common.lib.status      import Status, StatusList
from common.lib.http.status import *


class SlugNotFound(Status):
    def __str__(self):
        return 'ERR_SLUG_NOT_FOUND'

    def __init__(self, slug):
        super(SlugNotFound, self).__init__(100, HTTP_STATUS_NOT_FOUND,
              None, "We could not find a URL matching '%s'", slug) 


class SlugInUse(Status):
    def __str__(self):
        return 'ERR_SLUG_IN_USE'

    def __init__(self, slug):
        super(SlugInUse, self).__init__(101, HTTP_STATUS_BAD_REQ,
              None, "The custom slug '%s' is already " +
                    "used by someone else.", slug) 

class URLOpenFailed(Status):
    def __str__(self):
        return 'ERR_URL_OPEN_FAILED'

    def __init__(self, url, code):
        super(URLOpenFailed, self).__init__(102, HTTP_STATUS_NOT_FOUND,
              None, "Unable to open '%s': received error code %s. " +
                    "Are you sure this is a valid URL?", url, code) 


_STATUS_OBJECTS = [
    SlugNotFound(None),
    SlugInUse(None),
    URLOpenFailed(None, None),
]


class LooLuStatusList(StatusList):
    def __init__(self):
        super(LooLuStatusList, self).__init__()

        for obj in _STATUS_OBJECTS:
            self.append({'ident': str(obj), 'code': obj.code,
                         'http_status': obj.http_status,
                         'message': obj.msg_format})

