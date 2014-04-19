###
# GitAchievements Application - achievements.(coffee|js)
# author: Ford Peprah
# copyright (C) Git Achievements 2013-2014
#
# Dependencies:
#     jQuery   - jquery.js
#     select2  - select2.js
#     Backbone - exoskeleton.js
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
        if peices[i].length
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
        # Set up CSRF token for Ajax requests to allow us to perform
        # PUT/POST/PATCH requests from Ajax requests.
        csrftoken = @getCookie 'csrftoken'
        self = @

        $.ajaxSetup
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

    debugEnabled: () ->
        debug = parseInt @getQueryStringValue('debug'), 10
        debug > 0

    getQueryStringValue: (query) ->
        pattern = new RegExp("[\\?&]#{query}=([^&#]*)")
        results = pattern.exec(location.search)
        if results
            decodeURIComponent(results[1].replace(/\+/g, ' '))
        else
            ''

    addForm: (name, target) ->
        # Renders and adds the specified form the page
        name = name.toTitleCase()
        target = $(target || 'body').eq(0)
        form = new @Views["#{name}Form"]({
            'el': "form"
        })
        target.append(form.render().$el)
        @

    shuffle: (array) ->
        # Performs a FisherYates shuffle on an array and returns a new array
        # that has been randomized
        array = array.slice(0)
        index = 0
        currentIndex = array.length

        while currentIndex > 0
            index = Math.floor(Math.random() * currentIndex)
            currentIndex -= 1
            tmp = array[currentIndex]
            array[currentIndex] = array[index]
            array[index] = tmp

        array

    uniqueId: () ->
        # Generates a unique id by randomizing an array and concatenating from that
        # array a set of characters
        characters = 'abcdefghijklmnopqrstuvwxyz'.split('').concat('0123456789'.split(''))
        id = null
        maxlen = 10

        while id == null || $('#' + id).length
            id = @shuffle(characters).slice(0, maxlen).join("")

        id


###
# Placeholder for Views and Models
###
Application = new Application()
Application.Views = {}
Application.Models = {}


###
# Application Models
####
class Application.Models.Event extends Backbone.Model
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
        $.map eventData, ((value, key) ->
            attribute: key
            type: value
        )

    getJSON: () ->
        # We just need the event's attribute
        @model.get 'event-attribute'


class Application.Models.EventCollection extends Backbone.Collection
    # A collection of events that the Application supports
    url: API_ROOT.format('event')
    model: Application.Models.Event

    parse: (response) ->
        response.objects || []


class Application.Models.Quantifier extends Backbone.Model
    # A quantifier indicates how to handle multiple values
    getJSON: () ->
        @get 'id'


class Application.Models.QuantifierCollection extends Backbone.Collection
    # A collection of quantifiers
    url: API_ROOT.format('quantifier')
    model: Application.Models.Quantifier

    parse: (response) ->
        response.objects || []


class Application.Models.Method extends Backbone.Model
    # Different methods supported by the application, should be typechecked by the view
    # to ensure the attribute and method types match
    type: () ->
        @get('argument_type')

    getJSON: () ->
        # Since we can't create methods in forms, the "json" of a
        # method is just it's id.
        @get 'id'


class Application.Models.MethodCollection extends Backbone.Collection
    # Collection of methods/functions
    url: API_ROOT.format('method')
    model: Application.Models.Method

    parse: (response) ->
        response.objects || []


class Application.Models.Difficulty extends Backbone.Model
    getJSON: () ->
        @get 'id'


class Application.Models.DifficultyCollection extends Backbone.Collection
    url: API_ROOT.format('difficulty')
    model: Application.Models.Difficulty

    parse: (response) ->
        response.objects || []


class Application.Models.AchievementType extends Backbone.Model
    getJSON: () ->
        @get 'id'


class Application.Models.AchievementTypeCollection extends Backbone.Collection
    url: API_ROOT.format('achievementtype')
    model: Application.Models.AchievementType

    parse: (response) ->
        response.objects || []


class Application.Models.Condition extends Backbone.Model
    # Represents a generic condition, this class does not know what type of condiition
    # it represents, it's up for the callee to determine
    initialize: (opts) ->
        @set 'name', @get('description')

    getJSON: () ->
        $.extend true, {}, @attributes


class Application.Models.ConditionCollection extends Backbone.Collection
    # Collection of conditions; mostly used for custom conditions, may
    # be extended eventually for noral conditions
    url: API_ROOT.format('customcondition')
    model: Application.Models.Condition

    parse: (response) ->
        response.objects || []


class Application.Models.Badge extends Backbone.Model
    # Represents a Badge object
    getJSON: () ->
        name: @get('name'),
        description: @get('description')


###
# Application Views
###
class Application.Views.EventAttributeSelect extends Backbone.View
    # A EventAttributeSelect is a select of the various Event attributes
    # belonging to an event
    tagName: 'select'
    className: ''

    initialize: (opts) ->
        @parent = opts.parent

    getSelected: () ->
        selected = @$('option:selected')
        if selected then selected.val() else null

    onChange: () =>
        selected = @$('option:selected')
        @parent.trigger 'event:attribute:change',
            attribute: selected.val()
            type: selected.data('type')

    render: () ->
        # render, we add the attributes to the select box and initialize
        # the selectit box
        @$el = $(document.createElement(@tagName))
        for className in @className.split(' ')
            @$el.addClass(className)

        if @template
            @$el.html(@template.template(@model.attributes))
        else
            @$el.html()
        @$el.attr('id', Application.uniqueId())
        @$el.on('change', @onChange)
        @filter()

    filter: (type) ->
        # Apply the filter, if one exists, to determine which attributes can
        # be shown
        $el = @$el
        @$el.select2('destroy')
        @$el.children().remove()

        event_name = @model.get('name').replace(/[\._]/g, " ").toTitleCase()
        $.each @model.getAttributes(type), (index, attribute) ->
            name = attribute.attribute
            option = $('<option></option>')
                .val(attribute.attribute)
                .data('type', attribute.type)
                .text("#{event_name}'s #{name}")
            $el.append option

        @$el.select2()
        @


class Application.Views.DifficultySelect extends Backbone.View
    # Displays a sleect for a Difficulty collection, does not require a
    # template as it displays as a select
    tagName: 'select'

    initialize: (opts) ->
        @collection = new Application.Models.DifficultyCollection()
        @model = @collection
        @parent = opts.parent
        @changeTrigger = 'difficulty:change'

    onChange: (ev) =>
        model = @getSelected()
        @parent.trigger @changeTrigger, model

    getSelected: () ->
        selected = @$('option:selected')
        if !selected.length
            selected = @$el.children().eq(0)
            selected.prop('selected', true)
        cid = selected.val()
        @collection.get cid

    render: () ->
        # The model for this is actually a collection
        @$el = $(document.createElement(@tagName))
        self = @
        @collection.fetch().done () ->
            for model in self.collection.models
                option = $('<option></option>')
                option.val(model.cid)
                option.text(model.get('name').replace(/[\._]/g, ' ').toTitleCase())
                self.$el.append(option)

            if self.onRender
                self.onRender()

            self.$el
                .attr('id', Application.uniqueId())
                .select2
                    placeholder: 'Select an option'

            self.$el.on 'change', self.onChange
            self.$el.change()
        @


class Application.Views.MethodSelect extends Application.Views.DifficultySelect
    # Displays a select of methods
    initialize: (opts) ->
        @collection = new Application.Models.MethodCollection()
        @model = @collection
        @parent = opts.parent
        @changeTrigger = 'method:change'

    filter: (type) ->
        @$el.select2('destroy')
        @$el.children().remove()

        for model in @collection.models
            argument_type = model.get('argument_type')
            if type and argument_type and argument_type != type
                continue
            option = $('<option></option>')
            option.val(model.cid)
            option.text(model.get('name').toTitleCase())
            @$el.append(option)

        @$el.select2
            placeholder: 'Select a method'
        @


class Application.Views.EventSelect extends Application.Views.DifficultySelect
    initialize: (opts) ->
        @collection = new Application.Models.EventCollection()
        @model = @collection
        @parent = opts.parent
        @changeTrigger = 'event:change'


class Application.Views.QuantifierSelect extends Application.Views.DifficultySelect
    initialize: (opts) ->
        @collection = new Application.Models.QuantifierCollection()
        @model = @collection
        @parent = opts.parent
        @changeTrigger = 'quantifier:change'


class Application.Views.AchievementTypeSelect extends Application.Views.DifficultySelect
    # Essentially the same as a DifficultySelect excepts uses a different collection
    # and triggers a different thing
    initialize: (opts) ->
        @collection = new Application.Models.AchievementTypeCollection()
        @model = @collection
        @parent = opts.parent
        @changeTrigger = 'achievement:type:change'


class Application.Views.ConditionSelect extends Application.Views.DifficultySelect
    # Displays a select of conditions
    initialize: (opts) ->
        @collection = new Application.Models.ConditionCollection()
        @model = @collection
        @parent = opts.parent
        @changeTrigger = 'condition:change'

    onRender: () ->
        @$el.css('width', '100%')


class Application.Views.BadgeForm extends Backbone.View
    # Subform for creating a badge
    tagName: 'fieldset'
    template: '#badge-form'
    className: 'rounded-box'

    attachListeners: () ->
        @$el.on 'change keyup paste', 'textarea, input', @onChange
        @$el.on 'click', '.js-remove', () =>
            @parent.trigger 'badge:remove', @
            @remove()
        @

    initialize: (opts) ->
        @model.set('id', @model.cid)
        @model.set('name', "")
        @model.set('description', "")
        @parent = opts.parent

    # TODO: Add a badge preview option
    onChange: (ev) =>
        target = @$(ev.currentTarget)
        name = target.data('name')

        if target.is('textarea')
            @model.set(name || 'description', target.val())
        else
            @model.set(name || 'name', target.val())

    serialize: () ->
        @model.getJSON()

    render: () ->
        @$el = $(document.createElement(@tagName))
        @$el.html($(@template).html().template(@model.attributes))
        for className in @className.split(' ')
            @$el.addClass(className)

        @attachListeners()


class Application.Views.CustomConditionForm extends Backbone.View
    # A custom condition for simply has a selection that the user must choose
    # This is essentially a layout
    tagName: 'fieldset'
    template: '#custom-condition-form'
    className: 'rounded-box'
    regions:
        'condition': null

    initialize: (opts) ->
        @data = {}
        @parent = opts.parent

    render: () ->
        @$el = $(document.createElement(@tagName))
        for className in @className.split(' ')
            @$el.addClass(className)

        @$el.html($(@template).html().template({id: @id}))
        selector = if @regions.condition then @$(@regions.condition) else @$el

        condition = new Application.Views.ConditionSelect
            parent: @
        @on 'condition:change', @conditionChange

        @$el.on 'click', '.js-remove', () =>
            @parent.trigger 'custom:condition:remove', @
            @remove()

        selector.append(condition.render().$el)

        @

    conditionChange: (model) =>
        @data.condition = model.get('id')

    serialize: () ->
        id: @data.condition


class Application.Views.AttributeConditionForm extends Backbone.View
    # Subform for creating a attribute condition.  Has select(s) for multiple
    # attributes, and a select for the method.
    tagName: 'fieldset'
    template: '#attribute-condition-form'
    className: ''
    regions:
        'attribute': ".condition-attribute"
        'method': ".condition-method"
        'description': ".condition-description"
        'quantifier': ".condition-quantifier"

    initialize: (opts) ->
        @data = {}
        @parent = opts.parent

    addAttribute: () =>
        # Adds the select for a new event attribute to the attribute region
        view = new Application.Views.EventAttributeSelect
            model: @model
            parent: @
        @subviews.attribute ?= []
        @$(@regions.attribute)
            .append(view.render().$el)
            .append($('<br/>'))
        view.$el.css('width', '100%')
        @subviews.attribute.push(view)

        # Hack because the selects aren't rendering until they're filtered on
        # for some reason.
        if @subviews and @subviews.method
            @subviews.method.onChange()

        @

    render: () ->
        @$el = $(document.createElement(@tagName))
        self = @
        @subviews = {}

        for className in @className.split(' ')
            @$el.addClass(className)

        @$el.html($(@template).html().template($.extend true, {}, @model.attributes, {
            id: @id
        }))
        @$el.on 'click', '.js-add-attribute', @addAttribute
        @$el.on 'click', '.js-remove', () =>
            @parent.trigger 'attribute:condition:remove', @
            @remove()

        # Need a minimum of two attributes, so lets force the condition to
        # be populated with two selects
        @addAttribute()
        @addAttribute()

        # Render the subviews using the selector specified by the regions
        view = new Application.Views.MethodSelect
            parent: @
        @subviews.method = view
        @$(@regions.method).append(view.render().$el)
        view.$el.css('width', '100%')

        @on 'method:change', (method) =>
            for select in self.subviews.attribute
                select.filter(method.get('argument_type'))

        view = new Application.Views.QuantifierSelect
            parent: @
        @subviews.quantifier = view
        @$(@regions.quantifier).append(view.render().$el)
        view.$el.css('width', '100%')

        view = $('<input></input>')
        @$(@regions.description).append(view)
        @subviews.description = view

        @

    serialize: () ->
        attributes = []
        for attribute in @subviews.attribute
            attributes.push(attribute.getSelected())

        $.extend {},
            attributes: attributes
            method: @subviews.method.getSelected().get('id')
            description: @subviews.description.val()
            event_type: @model.get('id')
            quantifier: @subviews.quantifier.getSelected().get('id')


class Application.Views.ValueConditionForm extends Backbone.View
    # Subform for creating a value condition.  Has select for event attributes,
    # methods, and input for a value.
    tagName: 'fieldset'
    template: '#value-condition-form'
    className: 'rounded-box'
    regions:
        'attribute': ".condition-attribute"
        'value': ".condition-value"
        'method': ".condition-method"
        'description': ".condition-description"
        'quantifier': ".condition-quantifier"

    initialize: (opts) ->
        @data = {}
        @parent = opts.parent

    render: () ->
        self = @
        @$el = $(document.createElement(@tagName))

        for className in @className.split(' ')
            @$el.addClass(className)

        @$el.html($(@template).html().template($.extend true, {}, @model.attributes, {
            id: @id
        }))
        @$el.on 'click', '.js-remove', () =>
            @parent.trigger 'value:condition:remove', @
            @remove()

        @subviews = {}
        # Render the subviews using the selected specified by the regions
        view = new Application.Views.EventAttributeSelect
            model: @model
            parent: @
        @subviews.attribute = view
        @$(@regions.attribute).append(view.render().$el)
        view.$el.css('width', '100%')

        @on 'event:attribute:change', (attribute) =>
            self.subviews.method.filter(attribute.type)

        view = new Application.Views.MethodSelect
            parent: @
        @subviews.method = view
        @$(@regions.method).append(view.render().$el)
        view.$el.css('width', '100%')

        @on 'method:change', (method) =>
            self.subviews.attribute.filter(method.get('argument_type'))

        view = new Application.Views.QuantifierSelect
            parent: @
        @subviews.quantifier = view
        @$(@regions.quantifier).append(view.render().$el)
        view.$el.css('width', '100%')

        # We need to create two input objects to accept the description (name)
        # of the condition and the value it expects
        view = $('<input></input>')
        @$(@regions.value).append(view)
        @subviews.value = view

        view = $('<input></input>')
        @$(@regions.description).append(view)
        @subviews.description = view

        @

    serialize: () ->
        method: @subviews.method.getSelected().get('id')
        attribute: @subviews.attribute.getSelected()
        value: @subviews.value.val()
        event_type: @model.get('id')
        description: @subviews.description.val()
        quantifier: @subviews.quantifier.getSelected().get('id')


class Application.Views.AchievementForm extends Backbone.View
    # The main form used to create an achievement by adding together the subforms
    # for a badge, custom condition, value condition, and attribute condition
    tagName: 'form'
    template: '#achievement-form'
    className: ''
    post: "/achievement/create"
    method: "POST"

    regions:
        'conditions': "#conditions"
        'badge': "#badge"
        'type': "#type"
        'event': '#event'
        'description': "#description"
        'name': "#name"
        'difficulty': "#difficulty"
        'grouping': "#grouping"

    initialize: (opts) ->
        @data = {}

    attachListeners: () ->
        # Attach the DOM events
        @$el.on 'click', '.js-add-condition', @addCondition
        @$el.on 'click', '.js-add-badge', @addBadge
        @$el.on 'click', '#submit', @submit
        @on 'event:change', @eventChange

        # An achievement form has subforms in the way of views, we
        # attach a listener for the events that they trigger in the
        # parent view.
        @on 'difficulty:change', (model) =>
            @data.achievement ?= {}
            @data.achievement.difficulty = model.get('id')

        @on 'achievement:type:change', (model) =>
            @data.achievement ?= {}
            @data.achievement.type = model.get('id')

        @on 'badge:remove', () =>
            @addBadge()

        @on 'custom:condition:remove', (view) =>
            @data['custom-conditions'] = $.grep @data['custom-conditions'], (item) ->
                item.cid != view.cid

        @on 'attribute:condition:remove', (view) =>
            @data['attribute-conditions'] = $.grep @data['attribute-conditions'], (item) ->
                item.cid != view.cid

        @on 'value:condition:remove', (view) =>
            @data['value-conditions'] = $.grep @data['value-conditions'], (item) ->
                item.cid != view.cid

        # Setup Ajax with our CSRF Token
        Application.setupAjax()

        @

    eventChange: (model) =>
        @event = model
        @regions.conditions.empty()
        @

    addBadge: () =>
        if not @data.badge
            @data.badge = new Application.Views.BadgeForm
                model: new Application.Models.Badge()
                parent: @
            @regions.badge.append(@data.badge.render().$el)
        else
            @data.badge = null

    addCondition: (ev) =>
        form = undefined
        target = $(ev.currentTarget)
        name = target.data('condition')
        newId = @regions.conditions.children().length + 1

        if name == 'custom'
            @data['custom-conditions'] ?= []
            form = new Application.Views.CustomConditionForm
                id: newId
                parent: @
            @data['custom-conditions'].push(form)

        else if name == 'value'
            @data['value-conditions'] ?= []
            form = new Application.Views.ValueConditionForm
                id: newId
                model: @event
                parent: @
            @data['value-conditions'].push(form)

        else if name == 'attribute'
            @data['attribute-conditions'] ?= []
            form = new Application.Views.AttributeConditionForm
                id: newId
                model: @event
                parent: @
            @data['attribute-conditions'].push(form)

        else
            console.warn 'getConditionType called with unknown condition'

        if form != undefined
            @regions.conditions.append(form.render().$el)

    render: () ->
        # Render the form, the select it boxes, and the subform into the
        # DOM
        @$el = $(document.createElement(@tagName))
        @attachListeners()
        self = @

        for className in @className.split(' ')
            @$el.addClass(className)

        @$el.html($(@template).html().template())
        @$el.attr('method', @method)
            .attr('post', @post)

        # Turn the regions into jQuery selectors
        @regions.badge = @$(@regions.badge)
        @regions.conditions = @$(@regions.conditions)
        @regions.name = @$(@regions.name)
        @regions.description = @$(@regions.description)
        @regions.grouping = @$(@regions.grouping)

        # Render the subviews into their regions
        # First add a selector for determing the type of achievement
        select = new Application.Views.AchievementTypeSelect
            parent: @
        $el = select.render().$el
        region = @$(@regions.type)
        $el
            .css('width', "300px")
            .attr('name', region.attr('name'))
            .attr('id', region.attr('id'))
        region.replaceWith($el)

        # Add a selector for determining the difficulty of the achievement
        select = new Application.Views.DifficultySelect
            parent: @
        $el = select.render().$el
        region = @$(@regions.difficulty)
        $el
            .css('width', "300px")
            .attr('name', region.attr('name'))
            .attr('id', region.attr('id'))
        region.replaceWith($el)

        # Add a selector which determines the event this achievement expects
        # to be unlocked for.
        # TODO: Allow multiple events to be used
        select = new Application.Views.EventSelect
            parent: @
        $el = select.render().$el
        region = @$(@regions.event)
        $el
            .css('width', "300px")
            .attr('name', region.attr('name'))
            .attr('id', region.attr('id'))
        region.replaceWith($el)

        @regions.grouping.select2()
        @

    serialize: () ->
        # Return all the data from the subforms serialized as a JSON
        # object.
        data = $.extend true, {}, @data
        data.achievement = $.extend true, {}, data.achievement,
            name: @regions.name.val()
            description: @regions.description.val()
            grouping: @regions.grouping.val()

        if data.badge
            data.badge = data.badge.serialize()

        for condition in ['custom-conditions', 'value-conditions', 'attribute-conditions']
            if data[condition]
                # Map each condition to the serialized data
                data[condition] = $.map data[condition], (form) ->
                    form.serialize()

        data

    submit: (ev) =>
        # Prevent normal submit event from occuring
        ev.stopPropagation()
        ev.preventDefault()

        data = @serialize()

        $.ajax
            type: @method
            url: @post || window.location.pathname
            data: JSON.stringify(data)
            dataType: 'json'
            contentType: 'application/json'
            success: (response) ->
                # Note, success is not always success, it just implies that
                # the POST to the endpoint succeed, we have to validate that the response
                # was a success
                next = Application.getQueryStringValue('next')
                next = if next and next.length then next else '/achievement/vote'
                if (response.success)
                    window.location.pathname = next
                else
                    # If response is not successful, a validation error occurred, so
                    # add it to the error message field
                    msg = $('#error-message')
                        .html()
                        .template(response.response)
                    $(msg).appendTo('ul.messages')
                          .on('click', 'button', (ev) -> $(this).parent().remove())
            error: (response, textStatus, jqXHR) ->
                console.error textStatus


do (window, $ = window.$ || window.jQuery, Backbone = window.Backbone) ->
    window.App = Application
    console.log '%cGit Achievements', "color: #666; font-size: x-large; font-family 'Comic Sans', serif;"
    console.log '\u00A9 Ford Peprah, 2013-2014'
