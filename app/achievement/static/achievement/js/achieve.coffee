###
 * TODO: Finish the transition to exoskeleton.js
###


RegExp.escape = (s) ->
    # Escapes a string passed to it for consumption by
    # a Regexp constructor.
    # Reference: //stackoverflow.com/questions/3561493
    s.replace /[-\/\\^$*+?.()|[\]{}]/g, '\\$&'


String.prototype.format = () ->
    # Formats a string using {i} as a selector, similar to Python's
    # .format method.
    string = @
    replacements = Array.prototype.slice.call(arguments, 0)

    for i in [0..replacements.length - 1] by 1
        pattern = new RegExp(RegExp.escape("\{#{i}\}"), 'g')
        string = string.replace(pattern, replacements[i])

    string


String.prototype.template = (keywords) ->
    # Renders a template using syntax of <%= key %> as a
    # placeholder for where they value should be put
    string = @

    for key of keywords
        value = keywords[key]
        pattern = new RegExp("<%=\\s*#{key}\\s*%>", 'gi')
        string = string.replace(pattern, value)

    string.replace(/<\/?script>/g, '')


String.prototype.toTitleCase = () ->
    # Formats a string in titlecase
    string = @
    peices = string.split(" ")

    for i in [0..peices.length - 1] by 1
        peices[i] = peices[i][0].toUpperCase() + peices[i].substr(1)

    peices.join " "


String.prototype.trim = () ->
    # Fallback for browsers that don't support the trim() method
    # *cough* IE8 *cough* why are you using it *cough*
    @replace /^\s+|\s+$/gm, ''


# The API root for the application
API_ROOT = '/api/v1/{0}/'


class Application extends Object
    API_ROOT: API_ROOT

    constructor: (options) ->
        @$ = (window.$ || window.jQuery)
        @initializeEventData()

    getCookie: (name) ->
        cookieValue = null
        if document.cookie and document.cookie != ''
            cookies = document.cookie.split ';'
            for cookie in cookies
                cookie = cookie.trim()
                if cookie.substring(0, name.length + 1) == name + '='
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                    break
        cookieValue

    csrfSafeMethod: (method) ->
        # Methods that don't require CSRF protection
        /^(GET|HEAD|OPTIONS|TRACE)$/.test method

    sameOrigin: (url) ->
        # Test that a url is a same-origin url
        host = document.location.host
        protocol = document.location.protocol
        sr_origin = "//#{host}"
        origin = "#{protocol}#{sr_origin}"

        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            !(/^(\/\/|http:|https:).*/.test(url))

    setupAjax: () ->
        # Set up CSRF token for Ajax requests
        self = @
        csrftoken = @getCookie 'csrftoken'
        $.ajax
            beforeSend: (xhr, settings) ->
                if (!self.csrfSafeMethod(settings.type) && self.sameOrigin(settings.url))
                    # Send the token to same-origin, relative URLs only
                    # Send the token iff method warrants CSRF protection
                    # Use the CSRFToken value acquired earlier
                    xhr.setRequestHeader 'X-CSRFToken', csrftoken

    formatQueryStrings: (querystrings) ->
        # Encodes a dictionary of key-value pairs into query parameters
        query = ''
        for key, value of querystrings
            query += "#{key}=#{value}&"

        encodeURIComponent query

    fetch: (endpoint, querystrings, async) ->
        # Fetches data from the specified API endpoint either asynchronously
        # or synchronously.
        opts = {
            url: @API_ROOT.format(endpoint) + '?' + @formatQueryStrings(querystrings || {}),
            async: async,
            dataType: "json"
        }
        result = undefined

        if async == false and async != undefined
            $.ajax(opts).done (data) ->
                result = data
        else
            result = $.ajax(opts)

        result

    initializeEventData: () ->
        # Grabs the event data from the application's API
        @events = new Application.EventCollection()
        @events.fetch()


class Application.Event extends Backbone.Model
    # Represents an event/payload combination supported by the Application
    initialize: (opts) ->
        @name = opts.name
        @type = opts.id
        attributes = {}
        stack = []
        stack.push
            name: "",
            attributes: opts.attributes

        while stack.length > 0
            # Until we've exhausted the stack, assume whatever is ont he top of
            # the stack is an object.
            item = stack.shift()
            name = item.name

            for key, value of item.attributes
                # If we've reached a value that is a string, it means taht the current key,
                # we've reached an attribute
                if typeof value == 'string'
                    key = if name.length then "#{name}.#{key}" else key
                    attributes[key] = value
                else
                    stack.push
                        name: if name.length then "#{name}.#{key}" else key,
                        attributes: if $.isArray(value) then value[0] else value

        @set('event-attributes', attributes)

    getAttributes: (type) ->
        # Gets the different attributes that exist for that event, optionally
        # filtered by the expected argument type
        eventData = @get('event-attributes')
        if type
            tmp = {}
            $.each eventData, (key, value) ->
                if value == type
                    tmp[key] = value
            eventData = tmp
        $.map eventData, ((value, key) -> key)

    getJson: () ->
        # We just need the event's attribute
        @model.get 'event-attribute'


class Application.EventCollection extends Backbone.Collection
    # A collection of events that the Application supports
    url: API_ROOT.format('event')
    model: Application.Event

    parse: (response) ->
        response.objects || []


class Application.Method extends Backbone.Model
    # Different methods supported by the application, should be typechecked by the view
    # to ensure the attribute and method types match
    type: () ->
        @get('argument_type')

    getJson: () ->
        # Since we can't create methods in forms, the "json" of a
        # method is just it's id.
        @get 'id'


class Application.MethodCollection extends Backbone.Collection
    # Collection of methods/functions
    url: API_ROOT.format('method')
    model: Application.Method

    parse: (response) ->
        response.objects || []


class Application.Condition extends Backbone.Model
    # Represents a generic condition, this class does not know what type of condiition
    # it represents, it's up for the callee to determine
    getJson: () ->
        $.extend true, {}, @attributes


class Application.Badge extends Backbone.Model
    # Represents a Badge object
    getJson: () ->
        name: @get('name'),
        description: @get('description')


Application.Views = {}


class Application.Views.BadgeForm extends Backbone.View
    # Subform for creating a badge
    el: 'fieldset'
    template: '#badge_subform'
    className: ''
    events:
        'change input': "onChange"

    # TODO: Add a badge preview option
    onChange: (ev) ->
        target = @$(ev.currentTarget)
        name = target.attr('name')

        if target.is('textarea')
            @model.set(name, target.text())
        else
            @model.set(name, target.val())


class Application.Views.EventView extends Backbone.View
    # A EventView is a select of the various Event attributes
    # belonging to an event
    el: 'select'
    className: ''

    render: (type) ->
        # render, we add the attributes to the select box and initialize
        # the selectit box based on the passed filter
        $el = @$el
        $el.html(@template(@model.attributes))

        event_name = @model.get('name').replace(/\._/g, " ").toTitleCase()
        $.each @model.getAttributes(type), (attribute) ->
            name = attribute.replace(/\./g, "'s ").replace(/_/g, " ")
            option = $('<opton></option>')
                .attr('value', attribute)
                .text("#{event_name}'s #{name}")
            $el.append option

        @$el.select2()


class Application.Views.CustomConditionForm extends Backbone.View
    # A custom condition simply has a selection that ht euser must choose
    el: 'fieldset'
    template: '#custom_condition_subform'
    className: ''


do (window, $ = window.$ || window.jQuery, Backbone = window.Backbone) ->
    window.App = new Application()
