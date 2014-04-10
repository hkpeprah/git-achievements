import sys

from django.db import models


BUILT_IN = sys.modules['__builtin__']

ARGUMENT_TYPES = (
    ("None", "Any"),
    ("int", "Integer"),
    ("str", "String"),
    ("bool", "Boolean")
)


class BaseModel(models.Model):
    """
    Generic base model.
    """
    class Meta:
        abstract = True
        app_label = "assets"

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
        app_label = "assets"

    # Default to built in module
    modules = (
        BUILT_IN,
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

        try: # attempt to coerce type
            if self.argument_type is not None and \
               getattr(BUILT_IN, self.argument_type, None) is not None:

                cls = getattr(BUILT_IN, self.argument_type)
                for index, arg in enumerate(args[:]):
                    args[index] = cls(arg)

            else:
                cls = type(args[0])
                args = list(cls(arg) for arg in args)

        except (AttributeError, ValueError) as e:
            return None

        method = self.get_callable_method()

        # iterate over the supported modules
        for module in self.modules:
            try:
                if getattr(module, method, None) is not None:
                    return getattr(module, method)(*args)
            except TypeError:
                pass

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
        app_label = "assets"

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    custom = models.BooleanField(default=False)

    def is_custom(self):
        return self.custom

    def __unicode__(self):
        return self.name
