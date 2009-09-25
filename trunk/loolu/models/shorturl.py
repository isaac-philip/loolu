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

from google.appengine.ext import db
from django.core.cache import cache


class ShortURLCache(object):
    def __init__(self, shortURL):
        super(ShortURLCache, self).__init__()
        self.slug         = shortURL.slug
        self.privacy_code = shortURL.privacy_code
        self.long_url     = shortURL.long_url


class ShortURL(db.Model):
    time_added     = db.DateTimeProperty(verbose_name='Created',
                         auto_now_add=True)

    session_key    = db.StringProperty(verbose_name='Session Key')
    api_key        = db.StringProperty(verbose_name='API Key')

    subdomain      = db.StringProperty(verbose_name='Subdomain')
    host           = db.StringProperty(verbose_name='Host')

    slug           = db.StringProperty(verbose_name='Slug')
    custom_slug    = db.StringProperty(verbose_name='Custom Slug')
    privacy_code   = db.StringProperty(verbose_name='Privacy Code')

    short_url      = db.LinkProperty(verbose_name='Short URL')
    custom_url     = db.LinkProperty(verbose_name='Custom URL')

    notes          = db.StringProperty(verbose_name='Notes')

    utm_source     = db.StringProperty(verbose_name='UTM Source')
    utm_medium     = db.StringProperty(verbose_name='UTM Medium')
    utm_campaign   = db.StringProperty(verbose_name='UTM Campaign')
    utm_term       = db.StringProperty(verbose_name='UTM Term')
    utm_content    = db.StringProperty(verbose_name='UTM Content')

    long_url       = db.LinkProperty(verbose_name='URL',
                         required=True, indexed=True)

    final_url      = db.LinkProperty(verbose_name='Final URL')
    title          = db.StringProperty(verbose_name='Title', indexed=True)
    content_type   = db.StringProperty(verbose_name='Content Type')

    def __unicode__(self):
        return self.short_url

    def __str__(self):
        return self.short_url

    def to_dict(self):
        result = dict()

        result['time_added']   = self.time_added.strftime('%m/%d/%Y %H:%M:%S')

        result['long_url']     = self.long_url
        result['final_url']    = self.final_url

        result['slug']         = self.slug
        result['custom_slug']  = self.custom_slug

        result['short_url']    = self.short_url
        result['custom_url']   = self.custom_url

        result['utm_source']   = self.utm_source
        result['utm_medium']   = self.utm_medium
        result['utm_campaign'] = self.utm_campaign
        result['utm_term']     = self.utm_term
        result['utm_content']  = self.utm_content

        result['title']        = self.title
        result['notes']        = self.notes

        return result 

    @staticmethod
    def find_url(url, host=None, session_key=None, api_key=None,
                 title_null=True, **kwa):

        query = ShortURL.all()

        query.filter("long_url =", url)

        if not title_null:
            queryuery.filter("title !=", long_url)

        if host != None:
            query.filter("host =", host)

        if api_key != None:
            query.filter("api_key =", api_key)
        elif session_key != None:
            query.filter("session_key =", session_key)
 
        return query.get()
 
    @staticmethod
    def find_slug(host, slug):
        query = ShortURL.all()
        query.filter("host =", host)
        query.filter("slug =", slug)
        shortURL = query.get()
    
        if not shortURL:
            query = ShortURL.all()
            query.filter("host =", host)
            query.filter("custom_slug =", slug)
            shortURL = query.get()
   
        return shortURL

    @staticmethod
    def get_cache_key(host, slug):
        return '/cache/ShortURL/%s/%s' % (host, slug)  

    @staticmethod
    def get_cache(host, slug):
        return cache.get(ShortURL.get_cache_key(host, slug))
 
    def cache(self, time=0):
        data = ShortURLCache(self)

        cache.set(ShortURL.get_cache_key(self.host, self.slug), data, time)

        if self.custom_slug:
            cache.set(ShortURL.get_cache_key(self.host, self.custom_slug),
                data, time)

        return data
 
    def uncache(self):
        cache.delete(ShortURL.get_cache_key(self.host, self.slug))
    
        if self.custom_slug:
            cache.delete(ShortURL.get_cache_key(self.host, self.custom_slug))
  
