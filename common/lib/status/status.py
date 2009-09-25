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

from common.lib.http.status import *
from common.lib.serialize   import *


class Status(SerializableDict):
    def __str__(self):
        return 'ERR_NONE'

    def __init__(self, code=0, http_status=HTTP_STATUS_OK, param_name=None,
                 msg='No Error', *args):
        super(Status, self).__init__()
        self.code              = code
        self.http_status       = http_status
        self.msg_format        = msg
        self['code']           = code
        self['http_status']    = http_status 
        if param_name:
            self['param_name'] = param_name 
        self['message']        = msg % args 
        self['results']        = []

    def set(self, key, value):
        self[key] = value

    def is_success(self):
        return self['code'] == 0

    def append(self, status):
        if not self.get('errors'):
            self['errors'] = []
        self['errors'].append(status)

class InternalError(Status):
    def __str__(self):
        return 'ERR_INTERNAL_ERROR'

    def __init__(self, msg):
        super(InternalError, self).__init__(1, HTTP_STATUS_INT_ERROR,
              None, "Oh noes! We seemed to have experienced an internal " +
                    "error. Please try again later.")


class InvalidAPIMethod(Status):
    def __str__(self):
        return 'ERR_INVALID_API_METHOD'

    def __init__(self, method):
        super(InvalidAPIMethod, self).__init__(2, HTTP_STATUS_BAD_REQ, 
              None, "Invalid/unsupported API method: %s", method)


class InvalidAPIVersion(Status):
    def __str__(self):
        return 'ERR_INVALID_API_VERSION'

    def __init__(self, ver):
        super(InvalidAPIVersion, self).__init__(3, HTTP_STATUS_BAD_REQ, 
              None, "Invalid/unsupported API version: %s", ver)

class InvalidAPI(Status):
    def __str__(self):
        return 'ERR_INVALID_API'

    def __init__(self, api):
        super(InvalidAPI, self).__init__(4, HTTP_STATUS_BAD_REQ, 
              None, "Invalid/unsupported API: %s", api)

class InvalidAPIKey(Status):
    def __str__(self):
        return 'ERR_INVALID_API_KEY'

    def __init__(self, param_name, api_key):
        super(InvalidAPIKey, self).__init__(5, HTTP_STATUS_BAD_REQ, 
              param_name, "Invalid/disabled API key: %s", api_key)

class InvalidCredentials(Status):
    def __str__(self):
        return 'ERR_INVALID_CREDENTIALS'

    def __init__(self):
        super(InvalidCredentials, self).__init__(6, HTTP_STATUS_BAD_REQ, 
              None, "Invalid username/password")

class MissingParam(Status):
    def __str__(self):
        return 'ERR_MISSING_PARAM'

    def __init__(self, param_name, param_label):
        super(MissingParam, self).__init__(7, HTTP_STATUS_BAD_REQ,
              param_name, "Please provide a valid '%s'", param_label)

class InvalidParam(Status):
    def __str__(self):
        return 'ERR_INVALID_PARAM'

    def __init__(self, param_name, msg):
        super(InvalidParam, self).__init__(8, HTTP_STATUS_BAD_REQ,
              param_name, "%s", msg)

class NoChanges(Status):
    def __str__(self):
        return 'ERR_NO_CHANGES'

    def __init__(self):
        super(NoChanges, self).__init__(9, HTTP_STATUS_BAD_REQ,
              None, "No changes made.")


_STATUS_OBJECTS = [
    Status(),
    InternalError(None),
    InvalidAPIMethod(None),
    InvalidAPIVersion(None),
    InvalidAPI(None),
    InvalidAPIKey(None, None),
    InvalidCredentials(),
    MissingParam(None, None),
    InvalidParam(None, None),
    NoChanges(),
]


class StatusList(SerializableList):
    def __init__(self):
        super(StatusList, self).__init__()

        for obj in _STATUS_OBJECTS:
            self.append({'ident': str(obj), 'code': obj.code,
                         'http_status': obj.http_status,
                         'message': obj.msg_format})

