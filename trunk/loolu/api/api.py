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

from django.conf import settings 
from urllib2     import urlopen, URLError
from google.appengine.api.labs.taskqueue import taskqueue

from loolu.lib.status import *
from loolu.models     import ShortURL 
from loolu.forms      import ShortURLForm
from common.lib.html  import MetaParser 
from common.lib.http  import HTTP_STATUS_OK 
from common.lib.url   import URL


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
        if ip != '127.0.0.1' and ip != '76.20.0.241' and ip != '67.115.118.49':
            return InvitationOnly()

        try:
            urlData = None
 
            if request.GET.get('long_url') and getattr(
               settings, 'SPIDER_ENABLED', False) and not getattr(
               settings, 'SPIDER_IN_BACKGROUND'):
                urlData = self.fetch_url(request.GET.get('long_url'))

                if urlData and urlData.get('status_code') != HTTP_STATUS_OK:
                    return URLOpenFailed(request.GET.get('long_url'),
                                         urlData.get('status_code')) 

            form = ShortURLForm(request)
            if not form.is_valid():
                return form.status()

            api_key = request.GET.get('api_key') 
            if not api_key and not request.session.get('key', None):
                """
                To avoid a hit to the DB, we currently only create a session
                when a user shortens a URL. The following forces Django
                to allocate and save a session to the backend by assigning at
                least one session key
                """
                request.session['key'] = request.session.session_key

            """
            Form is valid, we have a session, now lets save the URL...
            """
            shortURL = form.save()

            if not shortURL:
                return InternalError()

            if not shortURL.content_type:
                if getattr(settings, 'SPIDER_ENABLED', False):
                    if not getattr(settings, 'SPIDER_IN_BACKGROUND'):
                        status = self.process_short_url(shortURL, urlData)
                    else:
                        taskqueue.add(url='/work/process_short_url/',
                            method='GET',
                            params=dict(url=shortURL.long_url,
                            host=shortURL.host,
                            slug=shortURL.slug))
   
            status.get('results').append(shortURL.to_dict())
        except:
            status = InternalError()
    
        return status

    def fetch_url(self, url):
        data = {
            'title':        None,
            'final_url':    None,
            'content_type': None,
            'status_code':  -1
        }

        try:
            f = urlopen(URL(url).str())

            data['final_url'] = f.geturl()
            data['status_code'] = HTTP_STATUS_OK

            if f.info().get('Content-type'):
                data['content_type'] = f.info().get('Content-type').lower()

            if data['content_type'].count('html'):
                p = MetaParser()
                p.parse(f.read())

                if p.title:
                    data['title'] = p.title
        except URLError, e:
            data['status_code'] = e.code
        except ValueError, e:
            data['status_code'] = -1
        except Exception, e:
            data['status_code'] = -1

        return data
 
    def process_short_url(self, shortURL, data=None):
        status = Status()

        try:
            modified = 0

            if not data:
                data = self.fetch_url(shortURL.long_url)

            if data.get('status_code') != HTTP_STATUS_OK:
                return URLOpenFailed(shortURL.long_url, data.get('status_code')) 
            if data.get('final_url') and shortURL.long_url != data['final_url']:
                modified += 1
                shortURL.final_url = data['final_url']
 
            if data.get('Content-type'):
                modified += 1
                shortURL.content_type = data['Content-type'].lower()

            if data.get('title'):
                modified += 1
                shortURL.title = data['title']
   
            if modified: 
                shortURL.put()  
        except:
            status = InternalError()

        return status
   
