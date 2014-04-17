import json
from django.test import TestCase
from django.contrib.auth.models import User

from app.services.models import Event
from app.achievement.utils import find_nested_json
from app.achievement.hooks import check_for_unlocked_achievements
from app.achievement.models import (Achievement, UserProfile, ConditionType, ValueCondition,
                                    Method, AchievementType, Difficulty, AchievementCondition,
                                    Qualifier, Quantifier, AttributeCondition)


class AchievementTestCase_01(TestCase):
    """
    Generic Achievement Test Suite to ensure they work.  Since all tests run in a transaction we
    don't have to worry about deleting the database objects created here.
    """
    def setUp(self):
        # Create the User object and other objects without relations
        user = User.objects.create(username="doug", password="password")
        difficulty = Difficulty.objects.create(name="easy", description="", points=1)
        equality = Method.objects.get_or_create(name="equal", callablemethod="__eq__")[0]
        push_event = Event.objects.get_or_create(name="push")[0]
        download_event = Event.objects.get_or_create(name="download")[0]

        # Create the types of Achievements and Conditions
        condition_type = ConditionType.objects.create(name="Non-custom", description="", custom=False)
        achievement_type = AchievementType.objects.create(name="Non-custom", custom=False)
        qualifier = Qualifier.objects.create(name="string length", description="", callablemethod="__len__", argument_type="str")
        quantifier = Quantifier.objects.create(name="any", description="", callablemethod="any", argument_type="list")

        # Create a value condition
        value_condition1 = ValueCondition.objects.create(description="Push was forced.", method=equality,
            condition_type=condition_type, attribute="action", value="forced", event_type=push_event)

        # Create an attribute condition and give it a qualifier
        attribute_condition1 = AttributeCondition.objects.create(description="Download's html_url same length as url", method=equality,
            event_type=download_event, condition_type=condition_type, attributes=["download.html_url", "download.url"])
        attribute_condition1.qualifiers.add(qualifier)

        # Create a value condition that uses a quantifier
        value_condition2 = ValueCondition.objects.create(description="Download file names are length 5.", method=equality,
            event_type=download_event, condition_type=condition_type, attribute="download.files.name", value="5",
            quantifier=quantifier, qualifier=qualifier)

        # Add an achievement that uses the value condition as it's condition
        achievement1 = Achievement.objects.create(name="I am the Heavy!", achievement_type=achievement_type,
            difficulty=difficulty, active=True, grouping="__and__", description="")

        achievement_condition1 = AchievementCondition.objects.create(content_object=value_condition1)
        achievement_condition1.achievements.add(achievement1)

        # Add an achievement that uses the attribute condition as it's condition
        achievement2 = Achievement.objects.create(name="Matching download urls length", achievement_type=achievement_type,
            active=True, grouping="__and__", description="", difficulty=difficulty)

        achievement_condition2 = AchievementCondition.objects.create(content_object=attribute_condition1)
        achievement_condition2.achievements.add(achievement2)

        # Add an achievement with multiple conditions as well as a condition that uses a quantifier
        # to ensure this works properly
        achievement3 = Achievement.objects.create(name="Any condition will do", achievement_type=achievement_type,
            active=True, grouping="__or__", description="", difficulty=difficulty)

        achievement_condition3 = AchievementCondition.objects.create(content_object=value_condition2)
        achievement_condition3.achievements.add(achievement3)
        achievement_condition2.achievements.add(achievement3)

    def test_profile_exists(self):
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
        self.assertTrue(len(unlocked) == 1, 'Achievement should be unlocked.')

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
        payload = {
            'download': {
                'files': [
                    {
                        'name': "a.txt"
                    },
                    {
                        'name': "b.txtp"
                    }
                ]
            }
        }

        self.assertEqual(["a.txt", "b.txtp"], find_nested_json(payload, "download.files.name".split('.')),
                         "Nested json results should match the values in the list.")

        unlocked = check_for_unlocked_achievements('download', payload)
        self.assertTrue(len(unlocked) == 1, 'Achievement was unlocked via quantifer and __or__')

    def test_qualifiers_01(self):
        """
        Tests that qualifiers actually work.
        """
        payload = {
            'download': {
                'url': "http",
                'html_url': "hfss"
            }
        }
        unlocked = check_for_unlocked_achievements('download', payload)
        self.assertTrue(len(unlocked) == 2, 'Achievement should be unlocked based on qualifier.')

        payload = {
            'download': {
                'url': "Http",
                'html_url': "https"
            }
        }
        unlocked = check_for_unlocked_achievements('download', payload)
        self.assertTrue(len(unlocked) == 0, 'Achievement should not be unlocked based on qualifier.')


class CustomConditionTestCase_01(TestCase):
    """
    Tests custom conditions.  For any custom condition added, it should have an equivalent test.
    """
    def setUp(self):
        pass
