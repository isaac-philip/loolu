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

import random

from google.appengine.ext import db
from django.core.cache import cache


class CounterShardData(db.Model):
    name  = db.StringProperty()
    value = db.IntegerProperty(default=0)


class CounterShard():
    key_name       = None
    key_name       = None
    cache_lifetime = None 
    cache_on_val   = None 

    def __init__(self, model_name, prop_name, key, num_shards=20,
                 cache_lifetime=60, cache_on_val=None):
        self.num_shards     = num_shards
        self.cache_lifetime = cache_lifetime
        self.key_name       = '/CounterShard/%s/%s/%s' % (model_name,
                              prop_name, key)

    def value(self, default=0):
        if self.cache_lifetime > 0:
            value = cache.get(self.key_name)
            if value != None:
                return value

        value = default
        for shard in CounterShardData.gql('WHERE name=:1', self.key_name):
            value += shard.value

        if self.cache_lifetime and (self.cache_on_val == None or
           value >= self.cache_on_val):
            cache.set(self.key_name, value, self.cache_lifetime)

        return value

    def incr(self):
        return self.change(1)

    def dec(self):
        return self.change(-1)

    def change(self, delta):
        def txn():
            shard_id = '%s:%s' % (self.key_name,
                  random.randint(1, self.num_shards))

            shard = CounterShardData.get_by_key_name(shard_id)
            if shard:
                shard.value += delta
            else:
                shard = CounterShardData(key_name=shard_id, name=self.key_name,
                              value=delta)

            shard.put()

        db.run_in_transaction(txn)

