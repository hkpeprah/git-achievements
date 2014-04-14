import json

from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter
def ith(array, i):
    """Returns ith element in list"""
    if i > len(array):
        return None
    return array[i]


@register.filter
def get_range(value):
    """
    Returns a range up to value.
    """
    return range(value)


@register.filter
def to_json(obj):
    """
    Returns a json of the object.
    """
    if hasattr(obj, 'to_json'):
        return obj.to_json()
    return json.dumps(obj)


@register.filter
def items(obj):
    """
    Returns an iterable of the object's items.
    """
    return obj.iteritems()

