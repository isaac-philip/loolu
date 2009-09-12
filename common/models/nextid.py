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

class NextID(db.Model):
    model_name = db.StringProperty()
    next_id    = db.IntegerProperty(default=1)

    @staticmethod
    def alloc(model_name):
        def alloc_in_txn(model_name):
            key_name = '/NextID/' + model_name
            nextID = NextID.get_by_key_name(key_name)
    
            if not nextID:
                nextID = NextID(key_name=key_name, model_name=model_name)
    
            nextID.next_id += 1
            nextID.put()
    
            return nextID.next_id - 1
   
        return db.run_in_transaction(alloc_in_txn, model_name)

