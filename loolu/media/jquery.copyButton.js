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

jQuery.fn.copyButton = function(settings){
    return this.each(function() {
        var button = $(this);

        settings = $.extend({
            input: null,

            initialTxt: 'Copy',
            successTxt: 'Copied!',

            onSuccess: function() {
                button.val(settings.successTxt); 
            },

            onError:   function() {
                settings.input.inlineError('Unable to copy to the clipboard.');
            },
        }, settings);


        $(this).val(settings.initialTxt);

        if (!FlashDetect.installed) {
            $(this).click(function() {
                settings.onError();
                return false;
            });
            return false;
        }

        var clip = new ZeroClipboard.Client();

        clip.setHandCursor(true);
        clip.setText(settings.input.val());
        clip.glue(button.attr('id'));
        clip.addEventListener('onComplete', settings.onSuccess);
    });
};
