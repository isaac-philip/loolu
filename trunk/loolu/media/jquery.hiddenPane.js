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

(function($)  {
    function onShow(event, updateCookie) {
        var settings = event.data;
        $(this).show();
        $(settings.link).text(settings.hideTxt);
        if (updateCookie) $.cookie('show_' + $(this).attr('id'), 1);
     }

    function onHide(event, updateCookie) {
        var settings = event.data;
        $(this).hide();
        $(settings.link).text(settings.showTxt);
        if (updateCookie) $.cookie('show_' + $(this).attr('id'), 0);
    }

    $.fn.showPane = function() {
        $(this).trigger('show', [false]);
    }

    $.fn.hidePane = function() {
        $(this).trigger('hide', [false]);
    }

    $.fn.hiddenPane = function(link, settings) {
        settings = $.extend({
            pane    : this,
            hidden  : true,
            showTxt : "Show",
            hideTxt : "Hide",
            cookies : true,
            link    : link
        }, settings);

        var pane   = settings.pane;
        var hidden = settings.hidden;

        if (settings.cookies) {
            hidden = ($.cookie('show_' + $(pane).attr('id')) != 1) ? 1 : 0;
        }

        $(pane).bind('show', settings, onShow);
        $(pane).bind('hide', settings, onHide);

        if (!hidden) {
            $(pane).trigger('show', [false]);
        } else {
            $(pane).trigger('hide', [false]);
        }

        $(link).click(function() {
            if ($(pane).css('display') == 'block') {
                $(pane).trigger('hide', [true]);
            } else {
                $(pane).trigger('show', [true]);
            }
        });
    };

    }
)(jQuery);
