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

from google.appengine.ext.db import djangoforms

from common.lib.status import Status, ValidationError


class ModelForm(djangoforms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

    def validate_regx(self, field, regx, msg):
        data  = self.cleaned_data
        value = data.get(field)

        if value and not re.compile(regx).match(value):
            raise ValidationError(msg)

        return data[field]

    def validate_len(self, field, min, max):
        data  = self.cleaned_data
        value = data.get(field)

        if min != None and (value == None or len(value) < min): 
            raise ValidationError(_(u"Value must be at least " +
                                     unicode(min) + " characters in length."))

        if max != None and value != None and len(value) > max: 
            raise ValidationError(_(u"Value can not exceed " +
                                     unicode(max) + " characters in length."))

        return data[field]

    def status(self):
        status = Status()

        if self.is_valid():
            return status 

        for p in self.errors:
            for e in self.errors[p]:
                if status.is_success():
                    status = ValidationError(p, unicode(e))
                else:
                    status.append(ValidationError(p, unicode(e)))

        return status

