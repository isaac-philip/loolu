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

from google.appengine.api import memcache

from django.http import HttpResponse, Http404, HttpResponsePermanentRedirect

from common.lib.counter  import CounterShard
from loolu.models import ShortURL 


def expand(request, slug, privacy_code=None):
    host = request.get_host() 
    key = '/memcache/ShortURL/%s/%s' % (host, slug)

    cache = memcache.get(key)
    if not cache:
        shortURL = ShortURL.find_slug(host, slug)
        if shortURL:
            cache = {'url':  shortURL.long_url,
                     'slug': shortURL.slug,
                     'code': shortURL.privacy_code}

            memcache.set(key, cache)

    if not cache:
        raise Http404

    if cache.get('code') and privacy_code != cache.get('code'):
        raise Http404

    counter = CounterShard('ShortURL', host, cache['slug'])
    counter.incr()

    return HttpResponsePermanentRedirect(cache['url'])

