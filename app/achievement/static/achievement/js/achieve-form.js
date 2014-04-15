/**
 * achieve-form.js - Git Achievements
 * author: Ford Peprah
 */

function getCookie(name) {
    /**
     *
     */
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

(function (window, $, FormData) {
    /* Closure as we want our own references to the window and
       jQuery ($) object. */
    var GitAchievements,
        condition_id = 1,
        csrftoken = getCookie('csrftoken');

    function BadgeForm (opts) {
        /**
         * Form for creating a Badge for an Achievement.
         * @constructor
         */
        $.extend(this, {
            template: "#badge",
            initialize: function (opts) {
                /**
                 * First method called, readies the form
                 */
                opts = opts || {};
                $.extend(this, opts);
            },
            render: function () {
                /**
                 * Called to generate the form DOM element, uses the
                 * template function to populate the HTML element with itself
                 * as context.
                 */
                var template = $(this.template);
                template = template.html().template(this);
                this.$el = $('<div></div>')
                    .append($(template));
                this.onRender();
                return this;
            },
            toJson: function () {
                /**
                 * Renders the json data in the form.
                 */
                var $el = this.$el;
                return {
                    name: $el.find('#badge-name').text(),
                    description: $el.find('#badge-description').text()
                };
            },
            onRender: function () {
                /**
                 * Called when the form is being rendered.  Adds additional
                 * data or does additional things.
                 */
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
                /**
                 * First method called, should ready the form
                 */
                opts = opts || {};
                $.extend(this, opts);
                this.id = condition_id;
                condition_id += 1;
            },
            render: function () {
                /**
                 * Renders the specified template using the object itself
                 * as context.
                 */
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

    function ValueConditionForm (opts) {
        /**
         * Form for creating a Value Condition.
         * @constructor
         */
        opts = $.extend({
            template: "#value-cond"
        }, opts);

        $.extend(this, new ConditionForm(opts), {
            type: "value",
            toJson: function () {
                /**
                 * Renders the form data on json.
                 */
                var $el = this.$el;
                return {
                    description: $el.find('input').eq(0).val(),
                    attribute: $el.find('select').eq(0).val(),
                    method: $el.find('select').eq(1).val(),
                    value: $el.find('input').last().val(),
                    event_type: $el.find('select').eq(0).find(':selected').data('event-type')
                };
            },
            onRender: function () {
                /**
                 * OnRender called when the form is being rendered.  Fetch the possible
                 * methods, and populate the attribute field with the event attributes.
                 */
                var data,
                    self,
                    $el = this.$el,
                    method = $el.find('select').eq(1),
                    attribute = $el.find('select').eq(0);

                // Attach the possible attributes to the select box
                $.each(GitAchievements.events, function (index, obj) {
                    attribute.append($('<option></option>')
                        .attr('value', obj.value)
                        .data('type', obj.type)
                        .data('event-type', obj.event_type)
                        .text(obj.name));
                });

                data = GitAchievements.fetch('method', undefined, false);
                $.each(data.objects, function (index, obj) {
                    method.append($('<option></option>')
                         .attr('value', obj.id)
                         .data('type', obj.argument_type)
                         .text(obj.name));
                });

                $el.find('select').select2();
                return this;
            }
        });

        return this;
    };

    function CustomConditionForm (opts) {
        /**
         * Form for creating a Custom Condition.
         * @constructor
         */
        opts = $.extend({
            template: "#custom-cond"
        }, opts);

        $.extend(this, new ConditionForm(opts), {
            type: "custom",
            toJson: function () {
                /**
                 * Returns the form's data as json.
                 */
                var $el = this.$el;
                return {
                    id: $el.find('select').eq(0).val()
                };
            },
            onRender: function () {
                /**
                 * OnRender called when the SubForm is being rendered.  We fetch the
                 * available custom conditions to populate the select box.
                 */
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
                var self = this;
                opts = opts || {};
                $.extend(this, opts);

                this.fetch('event').done(function (data) {
                    self.events = [];
                    $.each(data.objects, function (index, obj) {
                        obj = self.getEventAttributes(obj);
                        self.events = self.events.concat(obj);
                    });
                });

                this.forms = {
                    'valueconditions': [],
                    'customconditions': [],
                    'attributeconditions': []
                };
                this.attachListeners();
                return this;
            },
            getEventAttributes: function (obj) {
                /**
                 * Gets the nested attributes for the supported event
                 * and returns an array containing a hash of that attribute
                 * and the type of data it returns.
                 *
                 * @param {Object} obj
                 */
                var item,
                    name,
                    stack = [],
                    events = [];
                stack.push({
                    name: "",
                    attributes: obj.attributes
                });

                while (stack.length > 0) {
                    // Until we've exhausted the stack, assume whatever is on the
                    // stack is an object.
                    item = stack.shift();
                    name = item.name;
                    item = item.attributes;

                    for (var key in item) {
                        // If we've reached a value as a string, it means at the current key,
                        // we've reached an attribute of the initial event.
                        if (typeof item[key] === "string") {
                            events.push({
                                event_type: obj.id,
                                value: (obj.name + "." + key).toLowerCase(),
                                name: (obj.name.replace(/\._/, " ").toTitleCase() + " " + key).replace(/[\.]+/g, " "),
                                type: item[key]
                            });
                        } else if ($.isArray(item)) {
                            stack.push({
                                name: name + "." + key,
                                attributes: item[key][0]
                            });
                        } else {
                            stack.push({
                                name: name + "." + key,
                                attributes: item[key]
                            });
                        }
                    }
                }
                return events;
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
                var self = this,
                    $body = $('body');

                $body.on('click', 'button.close', function () {
                    $(this).parent().remove();
                });

                $body.on('click', '#create-badge-button', function () {
                    var form = new BadgeForm(),
                        target = $(this).data('target');

                    self.forms.badge = form;
                    $(target).append(form.render().$el);
                    $(this).hide();
                });

                $body.on('click', '#add-custom-condition', function () {
                    var form = new CustomConditionForm(),
                        target = $(this).data('target');

                    self.forms.customconditions.push(form);
                    $(target).append(form.render().$el);
                });

                $body.on('click', '#add-value-condition', function () {
                    var form = new ValueConditionForm(),
                        target = $(this).data('target');

                    self.forms.valueconditions.push(form);
                    $(target).append(form.render().$el);
                });

                $body.on('click', 'input[type="submit"]', function (ev) {
                    var data = {
                        'valueconditions': [],
                        'attributeconditions': [],
                        'customconditions': [],
                        'achievement': {},
                        'badge': null
                    };
                    ev.preventDefault();
                    ev.stopPropagation();

                    // Get the achievement data
                    data.achievement.name = $('#achievement-name').val();
                    data.achievement.description = $('#achievement-description').val();
                    data.achievement.type = $('#achievement-type').val();
                    data.achievement.difficulty = $('#achievement-difficulty').val();
                    data.achievement.grouping = $('#achievement-grouping').val();

                    if (self.forms.badge) {
                        // If we have a badge, pass it as json
                        data.badge = self.forms.badge.toJson();
                    }

                    // Get the conditions and add them to the data object
                    $.each(self.forms.valueconditions, function (index, condition) {
                        data.valueconditions.push(condition.toJson());
                    });

                    $.each(self.forms.customconditions, function (index, condition) {
                        data.customconditions.push(condition.toJson());
                    });

                    $.ajax({
                        type: "POST",
                        url: window.location.pathname,
                        data: JSON.stringify(data),
                        dataType: "json",
                        contentType: "application/json",
                        success: function (response) {
                            var msg;
                            if (!response.success) {
                                msg = $('#error-msg').html().template(response.response);
                                $(msg).appendTo('ul.messages');
                            } else {
                                window.location.pathname = "/achievement/vote";
                            }
                        },
                        error: function (response, textStatus, jqXHR) {
                            console.error(textStatus);
                        }
                    });
                });

                this.selectBox();
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

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('body').ready(function () {
        console.log("%cGit Achievements", "color: #666; font-size: x-large; font-family: 'Open-Sans', sans-serif;");
        GitAchievements = new App();
    });
})(window, window.$ || window.jQuery, window.FormData);
