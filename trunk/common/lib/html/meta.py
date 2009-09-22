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
import sgmllib
from htmlentitydefs import codepoint2name, name2codepoint, entitydefs


class MetaParser(sgmllib.SGMLParser):
    def __init__(self):
        self.save  = False
        self.data  = ''
        self.title = ''
        self.meta  = dict()
        sgmllib.SGMLParser.__init__(self)

    def parse(self, s):
        self.feed(s)
        self.close()

    def clean(self, val):
        val = val.strip().replace('\n', '')
        val = re.compile('\s+').sub(' ', val)
        return val

    def save_bgn(self):
        self.save = True

    def save_end(self):
        self.save = False
        return self.data

    def start_meta(self, attr):
        key = ''
        val = ''

        for a in attr:
            if len(a) != 2:
                continue

            attr_name = a[0].lower()

            if attr_name == 'content':
                val = a[1]
            elif attr_name == 'http-equiv' or attr_name == 'name':
                key = a[1]

        if key and val:
            self.meta[key] = self.clean(val)

    def start_title(self, attr):
        self.save_bgn()

    def handle_data(self, data):
        if self.save:
            self.data += self.clean(data)
        else:
            self.data = ''

    def handle_charref(self, ref):
        self.handle_data('&#' + ref + ';')

    def handle_entityref(self, ref):
        if entitydefs.get(ref):
            self.handle_data(entitydefs[ref])

    def end_title(self):
        self.title = self.save_end()
    
