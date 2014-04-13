/**
 *
 */
(function (window, $) {
    /* Closure as we want our own references to the window and
       jQuery ($) object. */
    var condition_id = 1;

    function BadgeForm (opts) {
        /**
         * Form for creating a Badge for an Achievement.
         * @constructor
         */
        $.extend(this, {
            template: "#badge",
            initialize: function (opts) {
                opts = opts || {};
                $.extend(this, opts);
            },
            render: function () {
                var template = $(this.template);
                template = template.html().template(this);
                this.$el = $('<div></div>')
                    .append($(template));
                this.onRender();
                return this;
            },
            onRender: function () {
                var difficulty,
                    $el = this.$el,
                    badge = $el.find('.achievement-badge'),
                    name = $el.find('.name span').eq(1),
                    star = $el.find('.name span').eq(0);

                $el.find('#badge-name').change(function () {
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
                return this;
            }
        });

        this.initialize(opts);
        return this;
    };

    function ConditionForm (opts) {
        /**
         * Generic condition creation form.
         * @constructor
         */
        $.extend(this, {
            template: "#condition",
            initialize: function (opts) {
                opts = opts || {};
                $.extend(this, opts);
                this.id = condition_id;
                condition_id += 1;
            },
            render: function () {
                var template = $(this.template);
                template = template.html().template(this);
                this.$el = $('<div></div>')
                    .append($(template));
                this.onRender();
                return this;
            }
        });
        this.initialize(opts);
        return this;
    };

    function CustomConditionForm (opts) {
        /**
         * Form for creating a Custom Condition.
         * @constructor
         */
        var GitAchievements = window.GitAchievements;
        $.extend(this, new ConditionForm({
            template: "#custom-cond"
        }));

        $.extend(this, {
            onRender: function () {
                var option, 
                    self = this,
                    selector = this.$el.find('select');
                GitAchievements.fetch('customcondition').done(function (data) {
                    $.each(data.objects, function (index, obj) {
                        option = $('<option></option>')
                            .attr('value', obj.id)
                            .text(obj.description);
                        selector.append(option);
                    });
                });
                selector.select2();
                return this;
            }
        });

        return this;
    };

    function App (opts) {
        /**
         * The main GitAchievements application.
         * @constructor
         */
        $.extend(this, {
            API_ROOT: "/api/v1/{0}",
            initialize: function (opts) {
                /**
                 * Initialize the application.
                 *
                 * @param {Object} opts
                 */
                opts = opts || {};
                $.extend(this, opts);
                this.attachListeners();
            },
            formatQueryStrings: function (querystrings) {
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
            },
            fetch: function (endpoint, querystrings, async) {
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
                querystrings = this.formatQueryStrings(querystrings);
                opts = {
                    url: this.API_ROOT.format(endpoint) + "?" + querystrings,
                    async: async,
                    dataType: "json"
                };

                if (async === false) {
                    $.ajax(opts).done(function (data) {
                        result = data;
                    });
                    return result;
                }
                return $.ajax(opts);
            },
            attachListeners: function () {
                /**
                 * Attaches the main listeners for the page.
                 *
                 * @return {this}
                 */
                this.selectBox();
                $('body').on('click', '#create-badge-button', function () {
                    var form = new BadgeForm(),
                        target = $(this).data('target');
                    $(target).append(form.render().$el);
                    $(this).hide();
                }).on('click', '#add-custom-condition', function () {
                    var form = new CustomConditionForm(),
                        target = $(this).data('target');
                    $(target).append(form.render().$el);
                });
                return this;
            },
            'selectBox': function () {
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

                this.fetch("difficulty").done(function (data) {
                    populateSelect('#achievement-difficulty', data.objects);
                });

                this.fetch("achievementtype").done(function (data) {
                    populateSelect('#achievement-type', data.objects);
                });
                return this;
            }
        });

        this.initialize(opts);
        return this;
    };

    $('body').ready(function () {
        console.log("%cGit Achievements", "color: #666; font-size: x-large; font-family: 'Open-Sans', sans-serif;");
        window.GitAchievements = new App();
    });
})(window, window.$ || window.jQuery);
