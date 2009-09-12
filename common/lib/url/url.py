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

from cgi      import parse_qs
from urllib   import urlencode
from urlparse import urlparse, urlunparse

class URL(object):
   def __init__(self, url, protocol='http'):
       self._parse(url, protocol)

   def _parse(self, url, protocol):
       self.url      = None
       self.modified = 0
       self.qs       = None
       self.parts    = list(urlparse(url, protocol))
       self.protocol = self.parts[0]
       self.netloc   = self.parts[1]
       self.path     = self.parts[2]
       self.query    = self.parts[4]
       self.fragment = self.parts[5]

   def __str__(self):
       return self.str()

   def __unicode__(self):
       return self.str()

   def str(self):
       if self.url != None and not self.modified:
           return self.url

       if self.qs:
           self.parts[4] = ''
           for name in self.qs:
               k = '&' + name + '='
               v = k.join(self.qs[name])
               p = k + v
               self.parts[4] += p
           self.parts[4] = self.parts[4].lstrip('&')
    
       self.modified = 0
       self.url = urlunparse(self.parts)

       return self.url

   def param(self, name, value=None, overwrite=True):
       if not self.qs:
           self.qs = parse_qs(self.query)

       if value == None or name in self.qs and not overwrite:
           return self.qs.get(name)

       self.modified += 1

       if type(value) == type(list()):
           self.qs[name] = value
       else:
           self.qs[name] = [value]

       return self.qs.get(name)

