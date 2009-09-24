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

import sys

from django.conf import settings 
from urllib2     import urlopen, URLError
from google.appengine.api.labs.taskqueue import taskqueue

from loolu.lib.status import *
from loolu.models     import ShortURL 
from loolu.forms      import ShortURLForm
from common.lib.html  import MetaParser 


class API(object):
    version = '2.0.1'

    def __init__(self):
        super(API, self).__init__()

    def method_supported(self, method, api=None):
        return (method == 'GET')

    def error_list(self, *args, **kw):
        status = Status()
        status.set('results', LooLuStatusList())
        return status

    def expand(self, request, *args, **kw):
        host = request.get_host()
        slug = request.GET.get('slug')
        long_url = request.GET.get('long_url')
 
        if not long_url:
            key = slug
        else:
            key = long_url

        shortURL = ShortURL.find(host, key)
        if not shortURL:
            return SlugNotFound(key)

        status = Status()
        result = shortURL.to_dict()
        status.get('results').append(result)
       
        return status 
 
    def shorten(self, request, *args, **kw):
        status = Status()
        ip = request.META.get('REMOTE_ADDR')

        try:  
            form = ShortURLForm(request)
            if not form.is_valid():
                return form.status()

            """
            Web Sessions Only:
            Force Django to allocate and save the session key
            to the backend cache/DB/file by setting assigning
            at least one session key
            """
            api_key = request.GET.get('api_key') 
            if not api_key and not request.session.get('key', None):
                request.session['key'] = request.session.session_key

            """
            Form is valid, we have a session, now lets save the URL...
            """
            shortURL = form.save()

            if settings.SPIDER_ENABLED:
                if not settings.SPIDER_IN_BACKGROUND:
                    status = self.process_short_url(shortURL)
                else:
                    taskqueue.add(url='/work/process_short_url/', method='GET',
                          params=dict(url=shortURL.long_url, host=shortURL.host,
                          slug=shortURL.slug))
   
            status.get('results').append(shortURL.to_dict())
        except:
            status = InternalError(str(sys.exc_info()[1]))
    
        return status
  
    def process_short_url(self, shortURL):
        status = Status()

        try:
            f = urlopen(shortURL.long_url)

            if shortURL.long_url != f.geturl(): 
                shortURL.final_url    = f.geturl()
            if f.info().get('Content-type'):
                shortURL.content_type = f.info().get('Content-type').lower()

            if shortURL.content_type.count('html'):
                p = MetaParser()
                p.parse(f.read())

                if p.title:
                    shortURL.title = p.title

            shortURL.put()  
        except URLError, e:
            status = URLOpenFailed(shortURL.long_url, e.code) 
        except:
            status = InternalError(str(sys.exc_info()[1]))

        return status
   
