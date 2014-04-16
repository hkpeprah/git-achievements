import json
from django.test import TestCase
from django.contrib.auth.models import User

from app.services.models import Event
from app.achievement.hooks import check_for_unlocked_achievements
from app.achievement.models import (Achievement, UserProfile, ConditionType, ValueCondition,
                                    Method, AchievementType, Difficulty, AchievementCondition)


class AchievementTestCase(TestCase):
    """
    Generic Achievement Test Suite to ensure they work.
    """
    def setUp(self):
        # Create the User object and other objects without relations
        User.objects.create(username="doug", password="password")
        Difficulty.objects.create(name="easy", description="", points=1)

        # Create the types of Achievements and Conditions
        ConditionType.objects.create(name="Non-custom", description="", custom=False)
        AchievementType.objects.create(name="Non-custom", custom=False)

        # Create conditions and achievements and join the relationship between them
        ValueCondition.objects.create(description="Push was forced.", method=Method.objects.get(callablemethod="__eq__"),
            condition_type=ConditionType.objects.get(pk=1), attribute="action", value="forced",
            event_type=Event.objects.get(name="push"))
        Achievement.objects.create(name="", achievement_type=AchievementType.objects.get(pk=1),
            difficulty=Difficulty.objects.get(name="easy"), active=True, grouping="__and__", description="")
        AchievementCondition.objects.create(content_object=ValueCondition.objects.get(pk=1))
        AchievementCondition.objects.get(pk=1).achievements.add(Achievement.objects.get(pk=1))

    def test_profile_exits(self):
        u = User.objects.get(username="doug")
        self.assertTrue(len(UserProfile.objects.filter(user=u)) == 1, "Profile was created on user creation.")

    def test_condition_satisfied(self):
        """
        Tests that a condition can be properly
        satisfied.
        """
        condition = ValueCondition.objects.get(pk=1)
        passed = condition({"action": "forced"})
        self.assertTrue(passed, 'Condition should be satisfied.')

    def test_condition_not_satisfied(self):
        """
        Tests that a condition is not improperly
        satisfied.
        """
        condition = ValueCondition.objects.get(pk=1)
        passed = condition({"action": ""})
        self.assertTrue(not passed, 'Condition should not be satisfied.')

    def test_user_unlocks_achievement(self):
        """
        Tests that a user can unlock an achievement.
        """
        payload = {"action": "forced"}
        unlocked = check_for_unlocked_achievements('push', payload)
        self.assertTrue(len(unlocked) > 0, 'Achievement should be unlocked.')

    def test_user_does_not_unlock_achievement(self):
        """
        Tests that an achievement is not improperly
        unlocked.
        """
        payload = {"action": "forced"}
        unlocked = check_for_unlocked_achievements('pull_request', payload)
        self.assertTrue(len(unlocked) == 0, 'Achievement should not be unlocked for non-matching event.')
        payload = {"action": ""}
        unlocked = check_for_unlocked_achievements('push', payload)
        self.assertTrue(len(unlocked) == 0, 'Achievement should not be unlocked for non-matching value.')

    def test_quantifier_01(self):
        """
        Tests that quantifiers actually work.
        """
        pass

    def test_qualifiers_01(self):
        """
        Tests that qualifiers actually work.
        """
        pass
