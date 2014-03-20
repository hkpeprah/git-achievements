import re
import json
import random
import operator
from picklefield.fields import PickledObjectField

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, UserManager
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from app.assets.utils import find_nested_json
from app.assets.models.base_models import BaseModel, BaseCallableModel, BaseTypeModel
from app.assets.models.local_settings import (CUSTOM_ACHIEVEMENT_TYPES,
    ACHIEVEMENT_DIFFICULTY_LEVELS)


class Event(BaseModel):
    """
    Generic event model.
    """
    pass


class Difficulty(models.Model):
    """
    Generic Difficulty model.  Have ranks and associated points
    with the model.
    """
    class Meta:
        app_label = "assets"

    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    # TODO: Why not negative?
    points = models.PositiveIntegerField()

    def __unicode__(self):
        return self.name


class Badge(models.Model):
    """
    Generic Badge model.  Badges can be won by users.
    """
    class Meta:
        app_label = "assets"

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

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
        return self.name


class Method(BaseCallableModel):
    """
    Defines a function that can be applied to multiple arguments.
    """
    modules = (
        # List of modules from which functions are
        # available.
        operator,
        str,
        re,
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


class Condition(models.Model):
    """
    Defines a generic condition.  A condition is passed an event and
    determines if the event satisfies the condition; returning a
    boolean to indicate whether it did or not.
    """
    class Meta:
        abstract = True
        app_label = "assets"

    method = models.ForeignKey('Method')
    event_type = models.ForeignKey('Event')
    description = models.TextField(blank=True)
    condition_type = models.ForeignKey('ConditionType')

    @property
    def type(self):
        return self.event_type.name

    def is_custom(self):
        return self.condition_type.is_custom()

    def __call__(self, event, attribute=None):
        return True

    def __unicode__(self):
        return self.description


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
            if self.qualifier is not None:
                value = self.qualifier(value)
            satisfied = self.method(value, self.value)
            passed.append(satisfied)

        if self.quantifier is not None:
            passed = self.quantifier(passed)
        else:
            passed = all(passed)

        return passed


class AttributeCondition(Condition):
    """
    Defines an attribute condition; an attribute condition is one where the two
    attributes in the returned event are tested against each other.
    """
    attributes = PickledObjectField()
    qualifiers = models.ManyToManyField('Qualifier', blank=True, null=True)

    def __call__(self, event):
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
                if qualifiers[index] is not None:
                    data = qualifiers[index](data)

            results.append(data)

        # Call the method on the resultant set
        passed = self.method(*results)
        return passed


class AchievementType(BaseTypeModel):
    """
    Generic achievement type.
    """
    types = dict(CUSTOM_ACHIEVEMENT_TYPES)

    def __unicode__(self):
        return self.types.get(self.name)


class AchievementCondition(models.Model):
    """
    Creates the Many-to-Many relationshiop between Achievements and Conditions.  Conditiosn
    can have belong to multiple Achievements and Achievements can have multiple conditions.
    Forces uniqueness w.r.t. the relationship.  The relationship is generic in nature.
    """
    class Meta:
        app_label = 'assets'

    achievements = models.ManyToManyField('Achievement', related_name='conditions')
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    @property
    def condition(self):
        """
        Returns the condition this points to.
        """
        return self.content_object


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

    # Achievement fields: these are the main fields for an achievement
    active = models.BooleanField(default=False)
    difficulty = models.ForeignKey('Difficulty')
    achievement_type = models.ForeignKey('AchievementType')
    badge = models.OneToOneField('Badge', related_name='achievement', blank=True, null=True)
    creator = models.ForeignKey('UserProfile', related_name='created_achievements', blank=True, null=True)
    grouping = models.CharField(max_length=10, choices=CONDITION_GROUPING, default=DEFAULT_GROUPING)

    @property
    def points(self):
        """
        Number of points won by completing this achievement.
        """
        return self.difficulty.points

    @property
    def earned_count(self):
        """
        Returns the number of users who earned this achievement.
        """
        return self.users.count()

    @property
    def get_conditions(self):
        """
        Returns a list of the condition objects attached to this achievement.
        """
        conditions = list(condition.content_object for condition in self.conditions.all())
        return conditions

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
        event_type, payload = event['type'], event['payload']

        for cond in self.conditions:
            if cond.id not in satisfied:
                if not cond.type == event_type:
                    return False
                passed = grouping(passed, cond(payload))

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
    badges = models.ManyToManyField('Badge', related_name='users', blank=True, null=True)
    achievements = models.ManyToManyField('Achievement', related_name='users', blank=True, null=True)

    # TODO: Add social auth for Github
    # Use UserManager to get the create_user method, etc.
    objects = UserManager()
