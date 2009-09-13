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

from django.conf.urls.defaults import *
from ragendja.urlsauto import urlpatterns

handler500 = 'ragendja.views.server_error'

urlpatterns = patterns('django.views.generic.simple',
    (r'^url-shortener/$', 'direct_to_template',
     {'template': 'url-shortener.html'}),

    (r'^api/$', 'direct_to_template',
     {'template': 'api.html'}),
 
    (r'^privacy/$',       'direct_to_template',
     {'template': 'privacy.html'}),

    (r'^terms/$',         'direct_to_template',
     {'template': 'terms.html'}),
) + urlpatterns

urlpatterns = patterns('',
    ## / - Redirect => /url-shortener/
    (r'^$', 'common.views.permanent_redirect',
     {'redirect_to': '/url-shortener/'}),

    ## Expand Slug
    (r'^(?P<slug>[\w]+)$',
      'loolu.views.site.expand'),
    (r'^(?P<slug>[\w]+)[-](?P<privacy_code>[\w\d]+)$',
      'loolu.views.site.expand'),

    ## Task Queue Handlers
    (r'^work/process_short_url/$',  'loolu.views.work.process_short_url'),

    ## API 
    (r'^api/v(?P<ver>[\d\.]+)/(?P<protocol>(json|xml))/(?P<fxn>[\w-]+)/$',
      'loolu.views.api.handle_api_call'),

    (r'^api/(?P<protocol>(json|xml))/(?P<fxn>[\w-]+)/$',
      'loolu.views.api.handle_api_call', {'ver': None}),

    ## Reset DB
    (r'^hidden/reset_db/$', 'loolu.views.hidden.reset_db'),
) + urlpatterns
