from django.db import models


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
        __builtins__
    )

    # Base fields
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    callablemethod = models.CharField(max_length=50)
    argument_type = models.CharField(max_length=50, choices=ARGUMENT_TYPES,
        default=ARGUMENT_TYPES[0][0])

    def __call__(self, *args):
        """
        Iterates over the supported modules to find the function it
        should use.

        @param self: Method instance
        @param args: List of arguments
        @return: Boolean
        """
        try: # attempt to coerce type
            cls = getattr(__builtins__, self.argument_type)
            if cls is not None:
                for index, arg in enumerate(args[:]):
                    args[index] = cls(arg)
        except AttributeError, ValueError:
            return None

        method = self.get_callable_method()

        for module in self.modules: # iterate over the supported modules
            if getattr(module, method, None) is not None:
                return getattr(module, self.method)(*args)

        return None

    def get_callable_method(self):
        """
        Should be overrided by the subclasses to determine which field
        to get the method name to use.
        """
        raise callablemethod

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
