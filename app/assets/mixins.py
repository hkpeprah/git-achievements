import re
import functools


class NoQualfiierException(Exception):
    pass


class NoQuantifierException(Exception):
    pass


class BaseMixin():
    """
    Base Mixin to define functions used throughout mixins.
    """
    def get_methods(self):
        """
        Returns the methods this supports.
        """
        return self.methods


class MethodMixin(BaseMixin):
    """
    Method Mixin is a class meant to be inherited by other classes
    The goal of the mixin is to provide method called `method` that
    can be used to apply a binary/unary operator to item.
    """
    methods = (
        ('contains', 'string contains'),
        ('>', '>'),
        ('<', '<'),
        ('>=', '>='),
        ('<=', '<='),
        ('==', '=='),
        ('!=', '!='),
        ('divides', 'divisible by'),
        ('begins_with', 'begins with'),
        ('ends_with', 'ends with'),
    )
    binary_operators = dict((
        (">", "gt"),
        ("<", "lt"),
        (">=", "ge"),
        ("<=", "le"),
        ("==", "eq"),
        ("!=", "ne")
    ))

    def set(self, m):
        """
        Sets the method to be used on a call to call.

        @param m: String
        @return: None
        """
        self.method = m

    def call(self, value, other):
        """
        Calls the set method on the passed parameters.
 
        @param value: Object
        @param value: Object
        @return: Object
        """
        func = getattr(self.binary_operators, self.method, self.method)
        return self[func](value, other)

    def method(self, m, value, other):
        """
        Applies the specified method, defaulting to the class instance's
        method itself if not found in binary operators.

        @param m: String
        @param value: Object
        @param other: Object
        @return: Object
        """
        func = getattr(self.binary_operators, m, m)
        return self[func](value, other)

    # The defined Mixin methods.  Binary operators are
    # mapped to names based on conventions.
    def lt(self, value, other):
        return value < other

    def le(self, value, other):
        return value <= other

    def gt(self, value, other):
        return value > other

    def ge(self, value, other):
        return value >= other

    def eq(self, value, other):
        return value == other

    def ne(self, value, other):
        return not self.eq(value, other)

    def divides(self, value, other):
        return value % other == 0

    def contains(self, value, other):
        return re.match(value, other) == None

    def begins_with(self, value, other):
        return value.startswith(other)

    def ends_with(self, value, other):
        return value.endswith(other)


class QualifierMixin(BaseMixin):
    """
    Mixin for qualifiers that apply the given sublacss method
    to the passed data.
    """
    methods = (
        ('length', 'length'),
    )
    built_ins = dict((
        ("length", len),
    ))

    def apply(self, m, obj):
        """
        Applies the qualifier to the object.

        @param m: String
        @param obj: Object
        @return: Object
        """
        func = getattr(self.built_ins, m, None)
        func = getattr(self, m, None) if not func else func

        if not func:
            raise NoQualifierException("No qualifier found.")

        return func(self, obj)


class QuantifierMixin(BaseMixin):
    """
    Mixin for quantifiers that apply the given function to an
    interable.
    """
    methods = (
        ('one', 'atleast one contains'),
        ('all', 'all contains'),
    )
    def apply(self, m, obj):
        """
        Applies the quantifier to the object.

        @param m: String
        @param obj: Object
        @return: Boolean
        """
        func = getattr(self, m, None)

        if not func:
            raise NoQuantifierException("No quantifier found.")

        return func(self, obj)

    # Quantifier Methods

    def one(self, obj):
        """
        Return true if one item in list is true.
        """
        obj = filter(lambda x: x == True, obj)
        return len(obj) > 0

    def all(self, obj):
        """
        Returns true if all items in list are true.
        """
        obj = filter(lambda x: x == False, obj)
        return len(obj) == 0
