import json

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User as AuthUser
from django.contrib.contenttypes.models import ContentType

from app.assets.mixins import MethodMixin, QualifierMixin, QuantifierMixin


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

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return "%s" % self.name


class Title(BaseModel):
    """
    Generic title model.

    @fields: name, description, image, user
    """
    # image = models.ImageField(upload_to=None, default="")
    user = models.ForeignKey('User', related_name='title')

    def get_image(self):
        return self.image

    def __unicode__(self):
        return "%s" % self.name


class Method(BaseModel, MethodMixin):
    """
    Defines a method.  Uses a mixin to allow the method to be
    applied to the specified data.
    """
    function = models.CharField(max_length=50, choices=MethodMixin.methods)
    argument_type = models.CharField(max_length=50, choices=ARGUMENT_TYPES)

    def call(self, value, other):
        """
        Calls the method in this class on the passed data.  First
        coercing them to the type specified by this method.

        @param value: String
        @param other: String
        @return: Object
        """
        # Can only trust in this because of validation (hopefully)
        try:
            cls = getattr(__builtins__, self.argument_type)
            value = cls(value) if cls is not None else value
            other = cls(other) if cls is not None else value
        except AttributeError, ValueError:
            return None

        # Calls the method on the given values
        self.set(self.function)
        return super(Method, self).call(other, value)

    def __unicode__(self):
        return "%s: %s" % (self.name, self.argument_type)


class Qualifier(BaseModel, QualifierMixin):
    """
    Defines a qualifier.  Ueses a mixin to define which qualifier
    should be applied to the passed value.
    """
    function = models.CharField(max_length=50, choices=QualifierMixin.methods)
    argument_type = models.CharField(max_length=50, choices=ARGUMENT_TYPES)

    def apply(self, obj):
        # Coerce type if necessary
        try:
            cls = getattr(__builtins__, self.argument_type)
            obj = cls(obj) if cls is not None else obj
        except AttributeError, ValueError:
            return None

        return self.apply(self.function, obj)


class Quantifier(BaseModel, QuantifierMixin):
    """
    Defines a quantifier.  Uses a mixin to define how the passed
    array should be handled.
    """
    function = models.CharField(max_length=50, choices=QuantifierMixin.methods)

    def apply(self, obj):
        return self.apply(self.function, obj)


class ConditionType(BaseModel):
    """
    Generic types that conditions can have.
    """
    custom = models.BooleanField(default=False)

    def is_custom(self):
        return self.custom

    def __unicode__(self):
        return "%s" % self.name


class ConditionGroup(BaseModel):
    """
    A group of collections joined by ORs or ANDs.
    """
    # TODO: and/or for groups of conditions
    achievement = models.ForeignKey('Achievement', related_name='condition')

    def test(self, event):
        """
        """
        for cond in self.conditions:
            if not cond.test(event):
                return False
        return True


class Condition(BaseModel):
    """
    Defines a generic condition.  A condition is passed an event and
    determines if the event satisfies the condition; returning a
    boolean to indicate whether it did or not.
    """
    # TODO: with operator
    method = models.ForeignKey('Method')
    condition_type = models.ForeignKey('ConditionType')
    group = models.ForeignKey('ConditionGroup', related_name='conditions')

    def is_custom(self):
        return self.condition_type.is_custom()

    def test(self, event, attribute=None):
        return True


class ValueCondition(Condition):
    """
    Defines a value condition; a value condition is one where the attribute is
    checked against a predefined value.
    """
    attribute = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    qualifier = models.ForeignKey('Qualifier', blank=True, null=True)
    quantifier = models.ForeignKey('Quantifier', blank=True, null=True)

    def test(self, event, attribute=None):
        """
        Tests the condition against the value and returns
        True if it succeeds, otherwise false.

        @param event: JSON object of the event
        @return: Boolean
        """
        if self.is_custom():
            return False

        if not attribute:
            attribute = self.attribute

        keys = attribute.split('.') # Attribute is period delimitted key
        obj = event

        for i in range(0, len(keys)):
            key = keys[i]
            obj, new_key = event[key], ".".join(keys[i+1:])
            if type(obj) == list:
                passed = [self.test(o, new_key) for o in obj] # Call recursively
                passed = self.quantifier.apply(passed) # Apply quantifier
                return passed

        obj = self.qualifier.apply(obj) # Apply qualifier
        passed = self.method.call(self.value, obj)
        return passed

    def __unicode__(self):
        return "%s %s %s"%(self.attribute, self.method, self.value)


class AttributeCondition(Condition):
    """
    Defines an attribute condition; an attribute condition is one where the two
    attributes in the returned event are tested against each other.
    """
    attribute1 = models.CharField(max_length=200)
    attribute2 = models.CharField(max_length=200)
    qualifier1 = models.ForeignKey('Qualifier', blank=True, null=True, related_name='qualifier1')
    qualifier2 = models.ForeignKey('Qualifier', blank=True, null=True, related_name='qualifier2')

    def test(self, event, attribute1=None, attribute2=None):
        """
        Tests the condition by checking the two attributes; returning
        True if the condition succeeds, otherwise False.

        @param event: JSON object of the event
        @return: Boolean
        """
        if self.is_custom():
            return False

        attribute1 = attribute1 if attribute1 else self.attribute1
        attribute2 = attribute2 if attribute2 else self.attribute2

        value1 = event
        for k in attribute1.split('.'):
            value1 = value1[k]

        for k in attribute2.split('.'):
            value2 = value2[k]

        # Call the method on the attributes
        passed = self.method.call(self.qualifier1.apply(value1),
                                  self.qualifier2.apply(value2))
        return passed


class AchievementType(BaseModel):
    """
    Generic achievement type.
    """
    NORMAL = "NON"
    CUSTOM_TYPES = (
        ('NON', 'Non-custom'),
        ('SPC', 'Special'),
        ('CUS', 'Custom'),
    )

    custom = models.CharField(max_length=50, choices=CUSTOM_TYPES)

    def is_custom(self):
        """
        Returns if this is a custom type or not.
        """
        return self.custom != self.NORMAL

    def __unicode__(self):
        return "%s" % str(self.custom)


class Achievement(BaseModel):
    """
    Defines an achievement.  An achievement is made up of multiple conditions
    that must be satisfied in order for the condition to be achieved.

    @fields: name, description, creator, achievement_type, conditions
    """
    DIFFICULTY_LEVELS = (
        ('0', 'Easy'),
        ('1', 'Medium'),
        ('2', 'Hard'),
        ('3', 'Very Hard'),
        ('4', 'Impossible')
    )
    creator = models.ForeignKey('User', related_name='achievements')
    achievement_type = models.ForeignKey('AchievementType')
    difficulty = models.CharField(max_length=50, choices=DIFFICULTY_LEVELS)

    def is_custom(self):
        """
        Returns if the achievement is custom.
        """
        return self.achievement_type.is_custom()

    def get_conditions(self):
        """
        Returns the conditions attached to this achievement.

        @return: Array of Condition
        """
        pass

    def get_satisfied_conditions(self, event):
        """
        Returns a list of the conditions that are satisfied by the
        event.

        @param event: Object
        @return: Array of Condition
        """
        satisfied = []
        for condition in self.conditions:
            if condition.test(event):
                satisfied.append(condition)
        return satisfied

    def unlocked(self, event):
        """
        Returns true if the event satisfies all the conditions of the
        achievement.  Otherwise False.

        @param event: Object
        @return: Boolean
        """
        return self.condition.test(event)

    def __unicode__(self):
        return "%s: %s"%(self.name, self.achievement_type)


class User(models.Model):
    """
    Defines a user object which has a one-to-one relation with the actual Django
    auth user.
    """
    # TODO: WRITE THIS
    # IDEA: STORE USERS PAST EVENTS, SO CAN CHECK FOR MORE COMPLICATED ACHIEVEMENTS
    #       e.g. Adding a 'with' option
    pass
