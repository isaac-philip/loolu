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

(function($)    {
    $.fn.inlineError = function(msg, field) {
        var errors = (typeof msg == 'string') ? [msg] : msg;
        var container = $(this).parent();
            
        field = (field) ? $('#' + field) : $(this);
        if (field.get() == '') {
            // Could not find the error field by ID, try
            // finding and using the "global" error list
            field = $('#errorlist');
        }

        if (field.get() == '') {
            // Could not find the form field OR the global error list,
            // so simply display a JavaScript alert() message
            alert(msg);
            return;
        }

        var errorClass = "errorlist";
        var errorlist = $(document.createElement("ul")).addClass(errorClass);

        field.prev(".errorlist").remove();
        field.before(errorlist.empty());

        for (var i in errors) {
            errorlist.append('<li class="error">' + errors[i] + '</li>');        
        }
     }

    function processAPIError(status) {
       if (!status.code)
            return; // Nothing to do

        var errors = new Array();

        if (!status.param_name)
            status.param_name = '__global__';
        errors[status.param_name] = new Array(status.message);

        if (status.errors) {
            // Multiple errors 
            for (var i in status.errors) {
               var error = status.errors[i];
               if (!error.param_name)
                   error.param_name = '__global__';
               if (!errors[error.param_name]) 
                   errors[error.param_name] = new Array();
               errors[error.param_name].push(error.message);
            }
        }

        for (var field in errors) {
            $(this).inlineError(errors[field], field);
        }
    }

    function stateChanged(oldState, newState) {
        if (!oldState)
            return true;

        if (typeof oldState == 'string')
            return (oldState != newState);

        if (oldState.length != newState.length)
            return true;

        for (var i in oldState) {
            if (oldState[i] != newState[i])
                return true;
        }

        return false;
    }

    function loading(form, elem, show) {
        if (!elem)
            elem = $('#' + form.attr('id') + ' .loading');

        if (elem.get() == '')
            return;

        if (show)
            elem.removeClass('hide');
        else 
            elem.addClass('hide');
    }

    $.fn.bindEvent = function(settings) {
        var lastState = null;

        settings = $.extend({
            event          : 'submit',
            url            : $(this).attr('action'),
            method         : $(this).attr('method'),
            checkUnchanged : false,
            onValidateForm : null,
            onBindForm     : null,
            onAJAXSuccess  : null,
            onAJAXError    : null,
            onAPISuccess   : null,
            onAPIError     : null,
            fields         : null,
            elem           : null,
        }, settings);

        // Check to see if jquery.validation.js was included
        // If so, go ahead and load and initialize this module now
        if ($(this).validation) 
            $(this).validation();

        return this.each(function() {
            var form = $(this);
            var elem = (settings.elem) ? settings.elem : form;

            elem.bind(settings.event, function() {
                var params = null;
                var fields = settings.fields;

                if (settings.onBindForm) {
                    settings.onBindForm(form);
                }

                if (settings.onValidateForm && !settings.onValidateForm(form)) {
                    return false;
                }

                if (!fields) {
                    // Serialize and submit the entire form
                    params = form.serialize();
                } else {
                    // Serialize and submit only the fields specified
                    params = {};
                    for (var i in fields) {
                        var field = fields[i];
                        params[field] = $('#'+field).val();
                    }
                }

                if (settings.checkUnchanged) {
                    var prevState = lastState;

                    lastState = params;

                    if (!stateChanged(prevState, params)) {
                        form.inlineError('No changes made.', '__global__');
                        return false;
                    }
                }

                if (settings.event == 'submit') {
                    loading(form, settings.elem, true);
                }

                $.ajax({
                    async    : false,
                    data     : params,
                    dataType : 'json',
                    type     : settings.method,
                    url      : settings.url,

                    error: function(XHR, textStatus, errorThrown) {
                        if (settings.onAJAXError) {
                            settings.onAJAXError(form, textStatus);
                        }
                    },

                    success: function(data, textStatus) {
                        var status = data;

                        if (status.code != 0)    {
                            processAPIError(status);

                            if (settings.onAPIError) {
                                settings.onAPIError(form, data, textStatus);
                            }
                         } else {
                            $('#' + form.attr('id') + ' .errorlist').empty();

                            if (settings.onAPISuccess) {
                                settings.onAPISuccess(form, data, textStatus);
                            }
                         }

                        if (settings.onAJAXSuccess) {
                            settings.onAJAXSuccess(form, data, textStatus);
                        }
                    },
                });

                loading(form, settings.elem, false);

                return false;
            });
        });
    }
})(jQuery);
