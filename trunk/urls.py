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

import os

from django.contrib import admin
from django.conf.urls.defaults import *

from ragendja.urlsauto import urlpatterns
from ragendja.auth.urls import urlpatterns as auth_patterns


admin.autodiscover()

handler500 = 'ragendja.views.server_error'
base_path  = os.path.abspath(os.path.dirname(__file__)) 

urlpatterns = auth_patterns


# Redirects 
urlpatterns = patterns('django.views.generic.simple',
    # / => /url-shortener/
    (r'^$', 'redirect_to', {'url': '/url-shortener/', 'permanent': True}),
) + urlpatterns

# Static Files 
urlpatterns = patterns('',
    # robots.txt
    (r'^(?P<path>robots.txt)$', 'django.views.static.serve', {
      'document_root': os.path.join(base_path, 'loolu/media/txt/'),
      'show_indexes': False}),
) + urlpatterns

# Django Admin 
urlpatterns = patterns('',
    # Admin
    ('^admin/(.*)', admin.site.root),
    (r'^create_admin_user/$', 'loolu.views.admin.create_admin_user'),
) + urlpatterns

# App URLs 
urlpatterns = patterns('loolu.views',
    # Flat pages
    (r'^(?P<page>url-shortener)/*$', 'site.render_from_template'),
    (r'^(?P<page>faq)/*$',           'site.render_from_template'),
    (r'^(?P<page>api)/*$',           'site.render_from_template'),
    (r'^(?P<page>code)/*$',          'site.render_from_template'),
    (r'^(?P<page>terms)/*$',         'site.render_from_template'),
    (r'^(?P<page>privacy)/*$',       'site.render_from_template'),

    # Expand Slug
    (r'^(?P<slug>[\w\-]+)$',         'site.expand_slug'),
    (r'^(?P<slug>[\w\-]+)[+](?P<privacy_code>[\w\-]+)$',
      'site.expand_slug'),

    # Task Queue Handlers
    (r'^work/process_short_url/$',   'work.process_short_url'),

    # API 
    (r'^api/v(?P<ver>[\d\.]+)/(?P<protocol>(json|xml))/(?P<fxn>[\w-]+)/$',
      'api.handle_api_call'),
    (r'^api/(?P<protocol>(json|xml))/(?P<fxn>[\w-]+)/$',
      'api.handle_api_call', {'ver': None}),
) + urlpatterns

