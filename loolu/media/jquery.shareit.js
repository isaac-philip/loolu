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

/*
 * Service Field Object
 */
function ServiceField(label, maxLen) {
    return {
        label:  label,
        maxLen: maxLen
    };
}

/*
 * Share Service Object
 */
function ShareService(name, urlFmt, urlField, titleField, msgField) {
    return { 
        name:       name,
        urlFmt:     urlFmt,
        urlField:   urlField,
        titleField: titleField,
        msgField:   msgField,

        getShareURL: function(link, title, msg) {
            var url = urlFmt;

            if (!link)    link  = document.location.href;
            if (!title)   title = document.title;
            if (!msg) msg = '';

            url = url.replace('<URL>',   escape(link));
            url = url.replace('<TITLE>', escape(title));
            url = url.replace('<MSG>',   escape(msg));

            return url;
        }
    };
}


(function($) {
   var ShareIt = function() {
        var services = {};

        var addService = function(name, service) {
                services[name] = service;
            };

        var getService = function(name) {
                return services[name];
            };

        var shareForm = function(elem, settings) {
            settings = $.extend({
                url      : '',
                title    : '',
                msg      : '',
                moHint   : 'Post to ',
                services : services
            }, settings);

            $('#shareit_btn').click(function() {
                var id    = $("input[name='shareit_svc']:checked").val();
                var svc   = getService(id);

                if (!svc)
                    return;

                var url   = $('#shareit_url input[type=text]').val();
                var title = $('#shareit_title input[type=text]').val();
                var msg   = $('#shareit_msg textarea').val();

                window.open(svc.getShareURL(url, title, msg));

                return false;
            });
 
            $(elem).find('div.shareit').each(function() {
                // Build up the services
                if ($(this).find('ul').get() == '') {
                    var idx = 0;
                    var ul = $(document.createElement("ul"));

                    $(this).append(ul);

                    for (var id in settings.services) {
                        var svc = settings.services[id];
                        if (!svc) continue;

                        var input  = $(document.createElement("input"));
                        $(input).attr('type', 'radio');
                        $(input).attr('name', 'shareit_svc');
                        $(input).attr('id', 'shareit_' + id);
                        $(input).attr('value', id);
                        if (!idx)
                            $(input).attr('checked', 'checked');

                        var label  = $(document.createElement("label"));
                        $(label).attr('for', 'shareit_' + id);
                        $(label).attr('title', settings.moHint + svc.name);
                        $(label).append(svc.name);

                        var li  = $(document.createElement("li"));
                        $(li).addClass(id);
                        if (idx++ == 0)
                            $(li).addClass('first');
                        $(li).append(input);
                        $(li).append(label);

                        $(ul).append(li);
                    }
                }

                idx = 0;
                $(this).find('input[type=radio]').each(function() {
                    var id  = $(this).val()
                    var svc = getService(id);
                    
                    $(this).click(function() {
                        var url   = $('#shareit_url input[type=text]');
                        var title = $('#shareit_title input[type=text]');
                        var msg   = $('#shareit_msg textarea');

                        if (!svc.urlField) {
                            $('#shareit_url').addClass('hide');
                        } else {
                            $('#shareit_url').removeClass('hide');
                            $('#shareit_url label').text(
                                svc.urlField.label + ':');

                            if ($(url).val() == '')
                                $(url).val(settings.url);
                        }

                        if (!svc.titleField) {
                            $('#shareit_title').addClass('hide');
                        } else {
                            $('#shareit_title').removeClass('hide');
                            $('#shareit_title label').text(
                                svc.titleField.label + ':');

                            if ($(title).val() == '')
                                $(title).val(settings.title);
                        }

                        if (!svc.msgField) {
                            $('#shareit_msg').addClass('hide');
                        } else {
                            $('#shareit_msg').removeClass('hide');
                            $('#shareit_msg label').text(
                                svc.msgField.label + ':');

                            if ($(msg).val() == '')
                                $(msg).val(settings.msg);

                            $(msg).simplyCountable({
                                counter        : '#shareit_msg .counter',
                                countType      : 'characters',
                                countDirection : 'down',
                                maxCount       : svc.msgField.maxLen
                            });
                        }
                   });

                   if (!idx++)
                       $(this).trigger('click');
              });
            }); 
        }; 

        var buttonBlock = function(elem, settings) {
            settings = $.extend({
                url      : document.location.href,
                title    : document.title,
                msg      : '',
                moHint   : 'Post to ',
                services : services
            }, settings);

            $(elem).find('div.shareit').each(function() {
                // Build up the services
                if ($(this).find('ul').get() == '') {
                    var idx = 0;
                    var ul = $(document.createElement("ul"));

                    $(this).append(ul);

                    for (var id in settings.services) {
                        var svc = settings.services[id];
                        if (!svc) continue;

                        var a = $(document.createElement("a"));
                        $(a).attr('target', '_new');
                        $(a).attr('title', settings.moHint + svc.name);
                        $(a).append(svc.name);

                        var li  = $(document.createElement("li"));
                        $(li).addClass(id);
                        if (idx++ == 0)
                            $(li).addClass('first');
                        $(li).append(a);

                        $(ul).append(li);
                    }
                }

                $(this).find('li').each(function() {
                    var id  = $(this).attr('class').replace(/\s*first\s*/i, '');
                    var svc = getService(id);
                    var a   = $(this).find('a');

                    if (svc && $(a).get()) {
                        $(a).attr('href', svc.getShareURL(settings.url,
                            settings.title, settings.msg));
                    }
                });
            }); 
        }; 


        addService('twitter', new ShareService('Twitter',
            'http://twitter.com/home?status=<MSG>',
            null, null, new ServiceField('Tweet', 140)));

        addService('facebook', new ShareService('Facebook',
            'http://facebook.com/share.php?u=<URL>&t=<TITLE>',
            new ServiceField('URL', 2083),
            new ServiceField('Title (optional)', 0), null));

        addService('myspace', new ShareService('MySpace',
            'http://myspace.com/Modules/PostTo/Pages/?l=3&' +
            'u=<URL>&t=<TITLE>&c=<MSG>',
            new ServiceField('URL', 2083),
            new ServiceField('Title (optional)', 95),
            new ServiceField('Description (optional)', 340)));

        addService('reddit', new ShareService('Reddit',
            'http://reddit.com/submit?url=<URL>&title=<TITLE>',
            new ServiceField('URL', 2083),
            new ServiceField('Title', 0), null));

        addService('digg', new ShareService('Digg',
            'http://digg.com/submit?url=<URL>&'+
            'title=<TITLE>&bodytext=<MSG>',
            new ServiceField('URL', 255),
            new ServiceField('Title', 75),
            new ServiceField('Message', 255)));

        addService('stumbleupon', new ShareService('Stumbleupon',
            'http://stumbleupon.com/submit?url=<URL>',
            new ServiceField('URL', 2083), null, null));

        addService('delicious', new ShareService('delicious', 
            'http://del.icio.us/post?url=<URL>&' +
            'title=<TITLE>&notes=<MSG>',
            new ServiceField('URL', 2083),
            new ServiceField('Title', 0),
            new ServiceField('Notes', 0)));

        addService('google', new ShareService('Google',
            'http://google.com/bookmarks/mark?op=edit&' +
            'bkmk=<URL>&annotation=<MSG>&title=<TITLE>',
            new ServiceField('URL', 2083),
            new ServiceField('Title', 0),
            new ServiceField('Notes', 0)));

        addService('technorati', new ShareService('Technorati',
            'http://technorati.com/cosmos/search.html?url=<URL>',
            new ServiceField('URL', 2083), null, null));


        return {
            buttonBlock: buttonBlock,
            shareForm:   shareForm,
            addService:  addService,
            getService:  getService
        }
    }

    /*
     * ShareIt Singleton
     */
     $.ShareIt = new ShareIt();
})(jQuery);


