import json
import random
import urllib
import urllib2

from bs4 import BeautifulSoup

import search
from utils import pretty_print


class SoupBot(object):
    """
    SoupBot is a web crawling robot that uses BeautifulSoup to parse the pages by determining sections
    and context of content on the page.  It also provides functionality for finding specific peices
    of information on the web, on pages, or through searches.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes SoupBot and collects the formatters to use.
        """
        formatters = filter(lambda x: "Formatter" in x, dir(search))
        self.formatters = {}

        for formatter in formatters:
            cls = getattr(search, formatter)

            if "ResponseDataFormatter" in formatter:
                self.default_formatter = cls
            else: # Apply naming convention for formatter
                formatter = formatter.replace("Google", "").replace("Formatter", "")
                formatter = "G{0}{1}".format(formatter[0].lower(), formatter[1:])
                self.formatters[formatter] = cls

    def search(self, method, params, shuffle, *args):
        """
        Performs a search using the GoogleSearch API.

        @param self: SoupBot instance
        @param method: The method to perform
        @param params: Dictionary of parameters to pass for querystrings
        @param shuffle: Whether or not to shuffle the results
        @param args: Arguments to pass the method
        @return: json
        """
        api = search.GoogleSearch()
        method = getattr(api, method, None)

        if method is None:
            return {}

        results, cls = method(params, *args).get()

        if shuffle:
            random.shuffle(results)

        formatter = self.formatters.get(cls, self.default_formatter)()
        return formatter(results)

    def parse(self, url):
        """
        Parses a page and generates the context from the items on that page.  Context is generated
        by parsing for sections, related items, etc.

        @param self: SoupBot instance
        @param url: The url pointing to the page to parse
        @return: json
        """
        pass
