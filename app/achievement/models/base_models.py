import sys

from django.db import models


class BaseModel(models.Model):
    """
    Generic base model.
    """
    class Meta:
        abstract = True
        app_label = "achievement"

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return "%s" % self.name


class BaseCallableModel(models.Model):
    """
    Callable base model.
    """
    class Meta:
        abstract = True
        app_label = "achievement"

    BUILT_IN = sys.modules['__builtin__']
    ARGUMENT_TYPES = (
        ("None", "Any"),
        ("int", "Integer"),
        ("str", "String"),
        ("bool", "Boolean")
    )

    # Default to built in module
    modules = (
        sys.modules['__builtin__'],
    )

    # Base fields
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    callablemethod = models.CharField(max_length=50)
    argument_type = models.CharField(max_length=50, choices=ARGUMENT_TYPES, null=True, blank=True)

    def __call__(self, *args):
        """
        Iterates over the supported modules to find the function it
        should use.

        @param self: Method instance
        @param args: List of arguments
        @return: Boolean
        """
        args = list(args)

        # Attempt to coerce type
        try:
            argument_type = self.argument_type
            convert_to_class = None
            if argument_type is None:
                convert_to_class = type(args[0])
            else:
                convert_to_class = getattr(BUILT_IN, argument_type)
            args = list(convert_to_class(arg) for arg in args)
        except (AttributeError, ValueError):
            return None

        # iterate over the supported modules
        method = self.get_callable_method()
        for module in self.modules:
            try:
                return getattr(module, method)(*args)
            except (AttributeError, TypeError):
                continue

        return None

    def get_callable_method(self):
        """
        Should be overrided by the subclasses to determine which field
        to get the method name to use.
        """
        return self.callablemethod

    def __unicode__(self):
        """
        Returns name.
        """
        return "%s: %s" % (self.name, self.argument_type)


class BaseTypeModel(models.Model):
    """
    Handles storing of special types.
    """
    class Meta:
        abstract = True
        app_label = "achievement"

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    custom = models.BooleanField(default=False)

    def is_custom(self):
        return self.custom

    def __unicode__(self):
        return self.name
