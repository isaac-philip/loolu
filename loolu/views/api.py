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

import time

from django.http import HttpResponse

from loolu.api        import * 
from loolu.lib.status import *


def handle_api_call(request, ver, protocol, fxn):
    start  = time.time()
    arg    = request.GET
    status = None

    try:
        api = APIFactory.create(ver)
        if not api:
            status = InvalidAPIVersion(ver)
        elif not api.method_supported(request.method):
            status = InvalidAPIMethod(request.method)
        else:
            if fxn == 'error-list':
                status = api.error_list(request)
            elif fxn == 'version':
                status = Status() 
            elif fxn == 'expand':
                status = api.expand(request)
            elif fxn == 'shorten':
                status = api.shorten(request)
            else:
                status = InvalidAPI(fxn)
    except:
        status = InternalError()

    if api: status.set('api_version', api.version) 
    status.set('api_method', fxn)
    status.set('query', request.META.get('QUERY_STRING'))
    status.set('completed_in', time.time() - start)
    status.set('http_status', 200)
 
    return HttpResponse(status=status.get('http_status'),
                        content=status.serialize(protocol),
                        mimetype='application/%s' % protocol)

