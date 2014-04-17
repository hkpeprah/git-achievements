import json
from django.test import TestCase
from django.core import management
from django.contrib.auth.models import User

from app.services.models import Event
from app.achievement.utils import find_nested_json
from app.achievement.hooks import check_for_unlocked_achievements
from app.achievement.models import UserProfile, ValueCondition, AttributeCondition


def setUpModule():
    """
    Sets up all the test cases in the current test file.  Only runs once.  Use to load
    data that will be used here.
    """
    pass


class AchievementTestCase_01(TestCase):
    """
    Generic Achievement Test Suite to ensure they work.  Since all tests run in a transaction we
    don't have to worry about deleting the database objects created here.
    """
    def setUp(self):
        management.call_command('loaddata', 'app/achievement/tests/test_data_01.json', verbosity=0)

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
