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

from ragendja.settings_post import *

settings.add_app_media(
    'loolu-combined-%(LANGUAGE_CODE)s.js',

    'loolu/jquery.hiddenPane.js',
    'loolu/jquery.placeHolder.js',
    'loolu/jquery.shareit.js',
    'loolu/jquery.simplyCountable.js',

    'loolu/jquery.validation.js',
    'loolu/jquery.jsonForm.js',

    'loolu/flash_detect.js',
    'loolu/ZeroClipboard.js',
    'loolu/jquery.copyButton.js',

    'loolu/url-shortener.js',
    'loolu/init-page.js',
)

settings.add_app_media(
    'loolu-combined.css',
    'loolu/style.css',
    'loolu/boxy.css',
    'loolu/shareit.css',
)

settings.add_app_media(
    'loolu-ie6-combined.css',
    'loolu/ie6.css',
)

