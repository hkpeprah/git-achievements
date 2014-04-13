/**
 *
 */

RegExp.escape = function(s) {
    /**
     * Escapes a string passed to it for consumption by the RegExp
     * constructor.  Reference: http://stackoverflow.com/questions/3561493/
     *
     * @param {String} s
     * @return {String}
     */
    return s.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
};


String.prototype.format = function () {
    /**
     * Formats a string using {i} as selectors where i is an
     * Integer.  Replaces it with the corresponding string in the
     * arguments list.
     *
     * @return {String}
     */
    var patt,
        string = this,
        replacements = Array.prototype.slice.call(arguments, 0);

    // For each replacement text, replace the appropriately index
    // item
    for (var i = 0; i < replacements.length; ++i) {
        patt = new RegExp(RegExp.escape('{' + i + '}'), 'g');
        string = string.replace(patt, replacements[i]);
    }
    return string;
};


String.prototype.toTitleCase = function () {
    /**
     * Formats a string in titlecase.
     *
     * @return {String}
     */
    var string = this,
        peices = string.split(" ");

    for (var i = 0; i < peices.length; ++i) {
        peices[i] = peices[i][0].toUpperCase() + peices[i].substr(1);
    }

    return peices.join(" ");
};


(function (window, $) {
    /* Enclosure to prevent global scoping of Application */
    var App = new Object();
    App.API_ROOT = "/api/v1/{0}";
    App.TEMPLATE_CACHE = {};

    App.initialize = function (opts) {
        /**
         * Initialize the application.
         *
         * @param {Object} opts
         */
        var id;
        $('script[type="text/template"]').each(function () {
            id = $(this).attr('id');
            App.TEMPLATE_CACHE[id] = $(this).html();
            $(this).remove();
        });

        this.attachListeners();
        /* Form specific listeners, particularly for badges. */
        this.attachBadgeListener();
    };

    App.formatQueryStrings = function (querystrings) {
        /**
         * Formats dictioanry of key-value querystring parameters
         * into their encoded string uri component.
         *
         * @param {Object} querystrings
         * @return {String}
         */
        var result = "";
        $.each(querystrings, function (key, value) {
            result += "{0}={1}&".format(key, value);
        });
        return encodeURIComponent(result);
    };

    App.fetch = function (endpoint, querystrings, async) {
        /**
         * Fetches data from the API and returns either a deferred object
         * representing the request or the data itself.
         *
         * @param {String} endpoint
         * @param {Object} querystrings
         * @param {Boolean} async
         * @return {Object}
         */
        var opts,
            result;
        querystrings = querystrings || {};
        querystrings = App.formatQueryStrings(querystrings);
        async = async === undefined ? true : async;
        opts = {
            url: App.API_ROOT.format(endpoint) + "?" + querystrings,
            async: async,
            dataType: "json"
        };

        if (!async) {
            $.ajax(opts).done(function (data) {
                result = data;
            });
            return result;
        }

        return $.ajax(opts);
    };

    App.attachListeners = function () {
        /**
         * Attaches the main listeners for the page.
         *
         * @return {this}
         */
        var location = window.location,
            path = window.location.pathname;

        if ($('form').length !== 0) {
            this.selectBox();
        }

        $('body').on('click', 'button', function () {
            /**
             * On the click of a button, if that button is set to
             * render or remove a rendered template, we trigger here.
             */
            var obj,
                $el = $(this),
                create = $(this).data('create'),
                remove = $(this).data('remove'),
                target = $(this).data('target');

            if (create !== undefined) {
                obj = App.TEMPLATE_CACHE['create-' + create];
                if (obj !== undefined) {
                    obj = $(obj).attr('id', create);
                    $(target).append(obj);
                }
            } else if (remove !== undefined) {
                $(remove).remove();
            }
        });
        return this;
    };

    App.attachBadgeListener = function () {
        /**
         * Attaches listeners for creating badges.
         *
         * @return {this}
         */
        $('body').on('click', '#create-badge-button', function () {
            var difficulty,
                badge = $('.achievement-badge'),
                name = badge.find('.name span').eq(1),
                star = badge.find('.name span').eq(0);

            $('#badge-name').change(function () {
                name.text($(this).val());
            });

            $('#achievement-difficulty').change(function () {
                star.removeClass(difficulty);
                difficulty = $(this)
                    .find(':selected')
                    .text()
                    .toLowerCase();
                star.addClass(difficulty);
            }).change();

            $(this).hide();
        });
        return this;
    };

    App.selectBox = function () {
        /**
         * Add the selectbox instances for the given page; for now, that is
         * the creation page.
         *
         * @return {this}
         */
        var populateSelect = function (selector, data) {
            var option;
            selector = $(selector);
            if (data !== undefined) {
                $.each(data, function(index, obj) {
                    option = $('<option></option>');
                    option.attr('value', obj.id)
                          .text(obj.name.toTitleCase());
                    selector.append(option);
                });
            }
            selector.select2();
        };

        $('#achievement-grouping').select2();

        App.fetch("difficulty").done(function (data) {
            populateSelect('#achievement-difficulty', data.objects);
        });

        App.fetch("achievementtype").done(function (data) {
            populateSelect('#achievement-type', data.objects);
        });

        return this;
    };

    // Add window attributes if any

    $('body').ready(function () {
        console.log("%cGit Achievements", "color: #666; font-size: x-large; font-family: 'Open-Sans', sans-serif;");
        App.initialize();
    });
})(window, window.$ || window.jQuery);
