from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()
IGNORE_METHODS = ['join']


@register.simple_tag
def stringmethod(name, value, first=None, second=None, third=None):
    """"
    Creates a template filter.

    @param value: The passed string
    @param first: First argument
    @param second: Second argument
    @param third: Third argument
    @return: object
    """
    return make_filter(name)(value, first, second, third)
 
 
@stringfilter
def make_filter(name):
    """
    Creats a filter by returning a wrapped method to be used.

    @param name: String name of the method
    @return: function
    """
    def filter_(value, first=None, second=None, third=None):
        """
        Applies the specified method to the passed arguments, popping
        arguments on each iteration until the right number is found.

        @param value: The passed string
        @param first: First argument
        @param second: Second argument
        @param third: Third argument
        @return: object
        """
        args = [first, second, third]
        method = getattr(value, name)
 
        while True:
            try:
                return method(*args)
            except TypeError:
                args.pop(len(args) - 1)
 
    return filter_
 

def register_string_extras():
    """
    Iterates over the possible string methods and registers
    them.

    @return: None
    """
    for name in dir(u''):
        # Ignore all private string methods
        if name.startswith('_') or name in IGNORE_METHODS:
            continue
 
        # Create new template filters for all string methods that not yet added
        # to Django template built-ins
        register.filter(name, make_filter(name))

    return None


# Register the string extras
register_string_extras()
