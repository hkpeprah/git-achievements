import re
import json
import random
import operator
from picklefield.fields import PickledObjectField

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, UserManager

from app.assets.utils import find_nested_json
from app.assets.models.base_models import BaseModel, BaseCallableModel, BaseTypeModel
from app.assets.models.local_settings import (CUSTOM_ACHIEVEMENT_TYPES,
    ACHIEVEMENT_DIFFICULTY_LEVELS)


class Badge(models.Model):
    """
    Generic Badge model.  Badges can be won by users.
    """
    class Meta:
        app_label = "assets"

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    users = models.ManyToManyField('UserProfile', related_name='badges', blank=True, null=True)
    achievement = models.OneToOneField('Achievement', related_name='badge', blank=True, null=True)

    @property
    def difficulty(self):
        """
        Gets difficulty for the badge.  Difficulty is determined by the achievement
        the badge is attached to.  Defaults to randomly selected level.
        """
        difficulty = None

        if self.achievement is not None:
            difficulty = self.achievement.difficulty
        
        else: # Randomly assign a difficulty for viewing purposes
            difficulty = random.sample(ACHIEVEMENT_DIFFICULTY_LEVELS, 1)[0][1]

        difficulty = difficulty.lower()
        return difficulty

    def __unicode__(self):
        return "%s" % self.name


class Method(BaseCallableModel):
    """
    Defines a function that can be applied to multiple arguments.
    """
    modules = (
        # List of modules from which functions are
        # available.
        re,
        str,
        operator,
    )


class Qualifier(BaseCallableModel):
    """
    Defines a function that returns the attribute of a single
    argument.
    """
    modules = (
        str,
    )


class Quantifier(BaseCallableModel):
    """
    Defines a function that when applied to an iterable, tests
    that the condition is true for the specification.
    """
    pass


class ConditionType(BaseTypeModel):
    """
    Generic types that conditions can have.
    """
    pass


class Condition(BaseModel):
    """
    Defines a generic condition.  A condition is passed an event and
    determines if the event satisfies the condition; returning a
    boolean to indicate whether it did or not.
    """
    class Meta:
        abstract = True

    method = models.ForeignKey('Method')
    condition_type = models.ForeignKey('ConditionType')
    achievement = models.ForeignKey('Achievement', related_name='conditions', blank=True, null=True)
    users = models.ManyToManyField('UserProfile', related_name='satisfied_conditions', blank=True, null=True)

    def is_custom(self):
        return self.condition_type.is_custom()

    def __call__(self, event, attribute=None):
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

    def __call__(self, event):
        """
        Tests the event object against the condition value.

        @param event: JSON object of the event
        @return: Boolean
        """
        if self.is_custom():
            return False

        data = find_nested_json(event, self.attribute.split('.'))

        if data is None:
            return False

        # Apply quantifiers, qualifiers and call the appropriate
        # method.
        passed = []
        for value in data:
            satisfied = self.method(self.qualifer(value), self.value)
            passed.append(satisfied)

        passed = self.quantifier(passed)
        return passed

    def __unicode__(self):
        return "%s %s %s"%(self.attribute, self.method, self.value)


class AttributeCondition(Condition):
    """
    Defines an attribute condition; an attribute condition is one where the two
    attributes in the returned event are tested against each other.
    """
    attributes = PickledObjectField()
    qualifiers = models.ManyToManyField('Qualifier', blank=True, null=True)

    def __call__t(self, event):
        """
        Tests the condition by checking the two attributes; returning
        True if the condition succeeds, otherwise False.

        @param event: JSON object of the event
        @return: Boolean
        """
        if self.is_custom():
            return False

        results, qualifiers = [], self.qualifiers

        for (index, attribute) in enumerate(self.attributes):
            data = find_nested_json(event, attribute)

            if data is None:
                return None

            elif index < len(qualifiers):
                data = qualifiers[index](data)

            results.append(data)

        # Call the method on the resultant set
        passed = self.method(*results)
        return passed


class AchievementType(BaseTypeModel):
    """
    Generic achievement type.
    """
    def __init__(self, *args, **kwargs):
        super(AchievementType, self).__init__(*args, **kwargs)
        self.fields['name'].choices = CUSTOM_ACHIEVEMENT_TYPES


class Achievement(BaseModel):
    """
    Defines an achievement.  An achievement is made up of multiple conditions
    that must be satisfied in order for the condition to be achieved.

    @fields: name, description, creator, achievement_type, conditions
    """
    # Grouping of the conditions.  Allows ofr spcifying that a condition
    # or another condition can unlock this achievement; similarly for 'and',
    # 'xor', 'or', etc.
    DEFAULT_GROUPING = '__and__'
    CONDITION_GROUPING = (
        ('__and__', 'and'),
        ('__or__', 'or'),
        ('__xor__', 'xor'),
    )

    # Achievement fields
    creator = models.ForeignKey('UserProfile', related_name='achievements', blank=True, null=True)
    achievement_type = models.ForeignKey('AchievementType')
    difficulty = models.CharField(max_length=50, choices=ACHIEVEMENT_DIFFICULTY_LEVELS)
    grouping = models.CharField(max_length=10, choices=CONDITION_GROUPING, default=DEFAULT_GROUPING)

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
            if condition(event):
                satisfied.append(condition)
        return satisfied

    def unlocked(self, event, satisfied=[]):
        """
        Returns true if the event satisfies all the conditions of the
        achievement.  Otherwise False.

        @param event: Object
        @param satisfied: Array of satisfied condition ids
        @return: Boolean
        """
        passed = True
        grouping = getattr(bool, self.grouping)

        for cond in self.conditions:
            if cond.id not in satisfied:
                passed = grouping(passed, cond(event))

        return passed

    def __unicode__(self):
        return "%s: %s"%(self.name, self.achievement_type)


class UserProfile(User):
    """
    Defines a user's profile which inherits form the Django User Auth model to
    add additional fields and allow for social auth to satisfy as requirements for
    logging in.
    """
    class Meta:
        app_label = "assets"

    moderator = models.BooleanField(default=False)

    # TODO: Add social auth for Github

    # Use UserManager to get the create_user method, etc.
    objects = UserManager()
