/**
 * LooLu is Copyright (c) 2009 Shannon Johnson, http://loo.lu/
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 * 
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 * LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 * WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 **/

jQuery.fn.placeHolder = function(placeholder){
    return this.each(function() {
        if (!placeholder && this.title)
            placeholder = this.title;

        if (!placeholder)
            return;

       $(this).addClass('placeholder');

       $(this).attr('value', placeholder);
       $(this).attr('title', placeholder);

       $(this).focus(function() {
           $(this).removeClass('placeholder');
           if ($(this).attr('value') == placeholder)
               $(this).attr('value', '');
       });

       $(this).blur(function() {
           $(this).addClass('placeholder');
           if ($(this).attr('value') == '')
               $(this).attr('value', placeholder);
       });
  
       $(this).parents("form:first").submit(function(){
           var sel = ' .placeholder';

           if ($(this).attr('id')) {
               sel = '#' + $(this).attr('id') + sel;
           }

           $(sel).each(function() {
               if ($(this).attr('value') == placeholder) {
                   $(this).val('');
               }
           });
       });
    });
};

