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

import re

from django.conf              import settings 
from django.forms             import ValidationError
from django.utils.translation import ugettext_lazy as _
from google.appengine.api     import memcache

from common.lib.url        import URL
from common.lib.url        import URLHash
from common.forms          import ModelForm
from common.models.nextid  import NextID

from loolu.models.shorturl import ShortURL


class ShortURLForm(ModelForm):
    class Meta:
        model   = ShortURL
        exclude = ['time_added',
                   'short_url',
                   'custom_url',
                   'final_url',
                   'slug',
                   'title',
                   'content_type',
                   'session_key',
                   'api_key']

    def __init__(self, request):
        super(ShortURLForm, self).__init__(request.GET)
        self.request = request

    def clean_subdomain(self):
        data  = self.cleaned_data
        if not data.get('subdomain'):
            data['subdomain'] = settings.DEFAULT_SUBDOMAIN
        try:
            settings.SUBDOMAINS.index(data['subdomain'])
        except:
            raise ValidationError(_(u"Invalid value."))

        return data['subdomain']

    def clean_host(self):
        data  = self.cleaned_data

        data['host'] = self.request.get_host()
        if data['host'].find('localhost',0,9) == -1:
            data['host'] = re.sub('^[\w-]+.', '%s.' % data['subdomain'],
                                  data['host'])
        return data['host'] 

    def clean_custom_slug(self):
        data = self.cleaned_data
        slug = data['custom_slug']

        self.validate_len('custom_slug', None, settings.MAX_CUSTOM_NAME_LEN) 
        self.validate_regx('custom_slug', '^[\w]+$',
                           _(u"Custom slug '%s' may only contain letters," +
                              " numbers and underscores.") % slug)

        shortURL = ShortURL.find_slug(data['host'], slug)
        if shortURL:
            raise ValidationError(_(u"The custom slug '%s' is already " +
                                     "used by someone else.") % slug)
        return data['custom_slug']

    def clean_notes(self):
        return self.validate_len('notes', None,
                   settings.MAX_DESCRIPTION_LEN)

    def clean_privacy_code(self):
        self.validate_len('privacy_code', None, settings.MAX_PRIVACY_CODE_LEN) 
        return self.validate_regx('privacy_code', '^[\w-]+$',
                   _(u"Privacy code may only contain letters," +
                      " numbers, underscores and dashes."))

    def clean_utm_medium(self):
        data  = self.cleaned_data
        if data.get('utm_source') and not data.get('utm_medium'):  
            raise ValidationError(_(u"This field is required."))
        return data['utm_medium']

    def clean_utm_campaign(self):
        data  = self.cleaned_data
        if data.get('utm_source') and not data.get('utm_campaign'):  
            raise ValidationError( _(u"This field is required."))
        return data['utm_campaign']

    def clean_long_url(self):
        self.validate_len('long_url', 10, settings.MAX_URL_LEN) 

        data  = self.cleaned_data
        utm_url = URL(data['long_url'])

        if data.get('utm_source'):
            utm_url.param('utm_source',   data.get('utm_source'))
        if data.get('utm_medium'):
            utm_url.param('utm_medium',   data.get('utm_medium'))
        if data.get('utm_campaign'):
            utm_url.param('utm_campaign', data.get('utm_campaign'))
        if data.get('utm_term'):
            utm_url.param('utm_term',     data.get('utm_term'))
        if data.get('utm_content'):
            utm_url.param('utm_content',  data.get('utm_content'))

        data['long_url'] = utm_url.str() 

        return data['long_url']
 
    def save(self, *args, **kwargs):
        data     = self.cleaned_data
        request  = self.request 
        session  = request.session 
        sess_key = session.session_key
        api_key  = data.get('api_key')
        host     = data.get('host')
        uncache  = 0
        modified = 0

        shortURL = ShortURL.find_url(data['long_url'], host=data['host'],
                       sess_key=sess_key, api_key=api_key)

        if not shortURL:
            shortURL = super(ShortURLForm, self).save(*args, **kwargs)

        if data.get('privacy_code') and not shortURL.privacy_code:
            modified = uncache = 1
            shortURL.privacy_code = data['privacy_code']
            shortURL.short_url = shortURL.custom_url = None
 
        if api_key and not shortURL.api_key:
            modified = 1
            shortURL.api_key = api_key
        elif not shortURL.session_key:
            modified = 1
            shortURL.session_key = sess_key

        if not shortURL.slug:
            modified = 1
            id = NextID.alloc('ShortURL/%s' % host)
            shortURL.slug = URLHash().encode(id)

        if data.get('custom_slug') and not shortURL.custom_slug:
            modified = 1
            shortURL.custom_slug = data['custom_slug']

        if not shortURL.short_url:
            if not shortURL.privacy_code:
                shortURL.short_url  = 'http://%s/%s' % (host, shortURL.slug)
            else:
                shortURL.short_url  = 'http://%s/%s-%s' % (host,
                                      shortURL.slug, shortURL.privacy_code)

        if shortURL.custom_slug and not shortURL.custom_url:
            modified = 1
            shortURL.custom_slug = data['custom_slug']
            if not shortURL.privacy_code:
                shortURL.custom_url  = 'http://%s/%s' % (host,
                                       shortURL.custom_slug)
            else:
                shortURL.custom_url  = 'http://%s/%s-%s' % (host,
                                       shortURL.custom_slug,
                                       shortURL.privacy_code)

        if data.get('notes') or shortURL.notes:
            modified = 1
            shortURL.notes = data['notes']

        if data.get('utm_source') or shortURL.utm_source:
            modified = uncache = 1
            shortURL.utm_source   = data.get('utm_source')
            shortURL.utm_medium   = data.get('utm_medium')
            shortURL.utm_campaign = data.get('utm_campaign')
            shortURL.utm_term     = data.get('utm_term')
            shortURL.utm_content  = data.get('utm_content')
    
        if not modified:
            return shortURL
 
        shortURL.put()

        if uncache:
            key = '/memcache/ShortURL/%s/%s' % (host, shortURL.slug)  
            memcache.delete(key)
    
            if shortURL.custom_slug:
                key = '/memcache/ShortURL/%s/%s' % (host, shortURL.custom_slug) 
                memcache.delete(key)
    
        return shortURL
         
