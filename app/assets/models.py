import json

from django.db import models
from django.contrib.auth.models import User as AuthUser
from django.core.exceptions import ValidationError

from apps.assets.mixins import MethodMixin, QualifierMixin, QuantifierMixin


class BaseModel(models.Model):
    """
    Generic base model.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):
        return "%s" % self.name


class Title(BaseModel):
    """
    Generic title model.

    @fields: name, description, image, user
    """
    image = models.ImageField(upload_to=None, default="")
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
    method_name = models.CharField(max_length=50)
    arg_type = models.CharField(max_length=50)

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
            cls = getattr(__builtins__, self.arg_type)
            value = cls(value)
            other = cls(other)
        except AttributeError, ValueError:
            return None

        # Calls the method on the given values
        self.set(self.method_name)
        return super(Method, self).call(other, value)

    def __unicode__(self):
        return "%s: %s" % self.name, self.arg_type


class Qualifier(BaseModel, QualifierMixin):
    """
    Defines a qualifier.  Ueses a mixin to define which qualifier
    should be applied to the passed value.
    """
    method_name = models.CharField(max_length=50)
    arg_type = models.CharField(max_length=50)

    def __init__(self, obj, *args, **kwargs):
        super(*args, **kwargs)
        # Coerce type if necessary
        try:
            cls = getattr(__builtins__, self.arg_type)
            obj = cls(obj)
        except AttributeError, ValueError:
            return None

        return self.apply(self.method_name, obj)


class Quantifier(BaseModel, QuantifierMixin):
    """
    Defines a quantifier.  Uses a mixin to define how the passed
    array should be handled.
    """
    method_name = models.CharField(max_length=50)

    def __init__(self, obj, *args, **kwargs):
        super(*args, **kwargs)
        return self.apply(self.method_name, obj)


class ConditionType(BaseModel):
    """
    Generic types that conditions can have.
    """
    custom = models.BooleanField(default=False)

    def is_custom(self):
        return self.custom

    def __unicode__(self):
        return "%s" % self.name


class Condition(models.Model):
    """
    Defines a condition.  A condition is passed an event and determines
    if the event satisfies the condition; returning a boolean to indicate
    whether it did or not.

    @fields: attribute, value, method, condition_type, qualifier, quantifier, achievement
    """
    attribute = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    method = models.ForeignKey('Method')
    condition_type = models.ForeignKey('ConditionType')
    qualifier = models.ForeignKey('Qualifier', blank=True, null=True)
    quantifier = models.ForeignKey('Quantifier', blank=True, null=True)
    achievement = models.ForeignKey('Achievement', related_name='conditions')

    def is_custom(self):
        return self.condition_type.is_custom()

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
                passed = self.quantifier(passed) # Apply quantifier
                return passed

        obj = self.qualifier(obj) # Apply qualifier
        passed = self.method.call(self.value, obj)
        return passed

    def __unicode__(self):
        return "%s %s %s"%(self.attribute, self.method, self.value)


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

    custom = models.CharField(max_length=20, choices=CUSTOM_TYPES, default=NORMAL)

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
    creator = models.ForeignKey('User', related_name='achievements')
    achievement_type = models.ForeignKey('AchievementType')

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
        return self.conditions

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
        passed = True
        for condition in self.conditions:
            passed = passed and condition.test(event)
            if not passed:
                break
        return passed

    def __unicode__(self):
        return "%s: %s"%(self.name, self.achievement_type)


class User(models.Model):
    """
    Defines a user object which has a one-to-one relation with the actual Django
    auth user.
    """
    pass # TODO: WRITE THIS
