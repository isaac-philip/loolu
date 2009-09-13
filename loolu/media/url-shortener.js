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

jQuery.urlShortener = function() {
    var lastLongURL = null;
  
    var TAB_ATTRIBUTES = 0;
    var TAB_ANALYTICS  = 1;
    var TAB_SHARE      = 2;
  
    var onValidateForm = function(form) {
        return $(form).validate();
    };
  
    var onBindForm = function(form) {
        if ($('#long_url').val() == '' && lastLongURL) {
            $('#long_url').val(lastLongURL);
        }
    };
  
   var onURLShortened = function(form, status) {
        if (status.code || !status.results)
            return; 
  
        var result = status.results[0]
        var shortURL = result.custom_url ?
                       result.custom_url : result.short_url;
  
        lastLongURL = result.long_url;
   
        $('#results').show();
 
        var msg = (result.title) ? result.title + ' ' + shortURL : shortURL; 
        var destination = (result.long_url.length < 100)
                          ? result.long_url
                          : result.long_url.substr(0,100) + '...';
  
        $('#results .destination span').text(destination);
  
        $('#short_url').val(shortURL);
        $('#short_url').select();
        $('#copy').copyButton({'input': $('#short_url')});
  
        $('#long_url').placeHolder('Rock on! Got another long link I can ' +
                                   'shorten for ya?');
  
        $('#expanded_options').showPane();
        $('#tabs').tabs('enable', TAB_SHARE);
        $('#tabs').tabs('select', TAB_SHARE);

        $('#shareit_url input[type=text]').val(shortURL);
        $('#shareit_url input[type=text]').attr('disabled', 'disabled');
        $('#shareit_title input[type=text]').val(result.title);
        $('#shareit_msg textarea').val(msg);
        $('#shareit_msg textarea').trigger('keyup');
    };

    var shareItCfg = {
        services: {
            'twitter':  $.ShareIt.getService('twitter'),
            'facebook': $.ShareIt.getService('facebook'),
            'myspace':  $.ShareIt.getService('myspace')
        }
    };

    $.ShareIt.shareForm($('#shorten_form'), shareItCfg);
  
    $('#tabs').tabs();
    $('#tabs').tabs('select', TAB_ATTRIBUTES);
  
    $('#long_url').placeHolder('Example: http://en.wikipedia.org/wiki/' +
                               'Portal:Contents/Portals#' +
                               'Mathematics_and_logic');

    $('#long_url').attr('validation', 'required url');
  
    $('#shorten_form').bindEvent({
        event          : 'submit',
        url            : $('#shorten_form').attr('action'),
        method         : $('#shorten_form').attr('method'),
        onAPISuccess   : onURLShortened,
        onValidateForm : onValidateForm,
        onBindForm     : onBindForm,
        fields         : ['long_url', 'subdomain', 'custom_slug',
                          'privacy_code', 'notes', 
                          'utm_source', 'utm_medium', 'utm_campaign',
                          'utm_term', 'utm_content']
    });
  
    $('#expanded_options').hiddenPane(
        $('#show_expanded_options a'),
        {'showTxt': "Show Options", 'hideTxt': 'Hide Options'});
  
  
    $('#notes').simplyCountable({
        counter: '#notes_counter',
        countType: 'characters',
        maxCount: 100,
        countDirection: 'down'
    });
  
    var q = $.parseQuery();
    if (q.u) {
        $('#long_url').val(q.u);
        $('#shorten_form').submit();
    }
}; 
