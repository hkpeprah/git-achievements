import json
from django.test import TestCase
from app.services.scrapers import BaseScraper, GithubScraper


class ScraperTestCase(TestCase):
    def setUp(self):
        self.base_scraper = BaseScraper()
        self.github_scraper = GithubScraper()

    def test_can_connect(self):
        """
        Ensures we are connected to the Internet and can make a valid request.
        """
        code = self.base_scraper.open('http://docs.python.org/2/library/unittest.html').code
        body = self.base_scraper.open('http://docs.python.org/2/library/unittest.html').read()
        self.assertTrue(code == 200, 'Request succeeded.')
        self.assertTrue(len(body) > 0, 'Response body is not empty.')

    def test_scraper_sets_type(self):
        """
        Ensures scraper is setting the proper types for the objects.
        """
        obj = {
            'doge': {
                'int': 9001,
                'str': "hue",
                'bool': True,
                'int': 42
            }
        }

        self.base_scraper.traverse_json(obj, True)
        for key, value in obj['doge'].iteritems():
            self.assertEqual(key, value, 'Type mismatch for key an value: %s != %s'%(key, value))

    def test_github_scraper_01(self):
        """
        Ensure the github scraper can get a single object.
        """
        release_obj = self.github_scraper.parse_single('https://developer.github.com/v3/repos/releases/')
        self.assertTrue(len(release_obj) > 0, 'Scraped github event has content.')
        self.assertTrue(type(release_obj) == dict, 'Scraped github data is valid json.')
