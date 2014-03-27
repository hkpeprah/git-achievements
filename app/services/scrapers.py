import re
import json
import urllib
import urllib2
import urlparse
import mechanize
from bs4 import BeautifulSoup


class BaseScraper(mechanize.Browser):
    """
    Generic BaseScraper class that defines the base methods and operations
    required by the Github/Bitbucket/et. al scrapers to scrape the relevant JSON
    data from given pages.
    """
    def __init__(self, *args, **kwargs):
        # mechanize uses old style classes
        mechanize.Browser.__init__(self, *args, **kwargs)

    def get(self, url):
        """
        Get the content of the page pointed to by the passed
        url.

        @param url: String
        @return: String
        """
        response = self.open(url).read()
        return response

    def parse(self, url):
        """
        Return the contents of the page pointed to by the url
        as a JSON object.
        
        @param url: String
        @return: json
        """
        response = self.get(url)
        data = json.loads(response)
        return data

    def traverse_json(self, obj, to_type=False):
        """
        Consumes a dict or list of dicts and iterates over the the iterables
        until it reaches a non-iterable base class.

        @param obj: Object
        @param to_type: Boolean, indicates to store type or not
        @return: None
        """
        objs = obj[:] if type(obj) == list else [obj]

        while len(objs) > 0:
            o = objs.pop(0)
            if type(o) == dict: # If dict, may modify in-place
                for k, v in o.items():
                    if type(v) == dict:
                        objs += [v]
                    elif type(v) == list:
                        objs += v[:]
                    else:
                        o[k], cls = v, type(v).__name__.lower()
                        if to_type:
                            if cls == 'unicode' or cls == 'nonetype':
                                cls = "str"
                            o[k] = cls
            elif type(o) == list: # Append list items directly
                objs += o[:]

        return None


class GithubScraper(BaseScraper):
    """
    """
    root = "https://developer.github.com/v3/activity/events/types/"

    def get_type(self, cls):
        """
        Maps the passed class to the python equivalent class and returns
        that as a string.
        """
        clsses = {
            'integer': "int",
            'string': "str",
            'array': "list",
            'double': "float",
            'float': "float",
            'boolean': "bool"
        }
        return clsses.get(cls.lower(), cls.lower())

    def parse_single(self, url=None):
        """
        Parses a single passed page for the single json object that corresponds to
        the event of that given page.

        @param url: String
        @return: json
        """
        response = self.get(url)
        data, keys = {}, []
        soup = BeautifulSoup(response)

        for tag in soup.find_all('h2'):
            tag_id = tag.get('id', '')
            if tag_id and len(tag_id) > 0:
                keys.append(tag['id'])

        tags = soup.find_all('code', {'class': 'language-javascript'})
        for i in range(0, len(tags)):
            tag, key = tags[i], keys[i]
            if 'get' in key:
                if 'single' in key:
                    data = json.loads(tag.text)
                    break
                data = json.loads(tag.text)

        return data


    def parse(self, url=None, to_type=False):
        """
        Parses the entire api page to construct the structure of the event responses;
        stores the types of the data as the values.

        @param url: String
        @param to_type: Boolean, indicates whether to store text or type
        @return: json
        """
        url = url if url else self.root
        response = self.get(url)
        data = {}
        soup = BeautifulSoup(response)

        for tag in soup.find_all('code'):
            if not tag.parent or not tag.parent.name == "p":
                continue

            # Sibling is the payload table
            try:
                sibling = list(tag.parent.next_siblings)[1]
                tag_id = sibling['id']
                if not "payload" in tag_id:
                    continue
            except KeyError:
                continue
            except IndexError:
                continue

            # Next element is the actual table
            table = list(sibling.next_siblings)[1]
            key = tag.text
            data[key] = {}

            for tag in table.find_all('tr'):
                # For each key, add the result to the data object and parse the
                # pointed link if it exists
                if not tag.parent.name == "tbody":
                    continue

                cells = tag.findAll('td')
                attr, value, details = cells # key, type, description
                attr = attr.text

                if details.find('a'):
                    value = details.find('a')
                    href = value.get('href') if 'http' in value.get('href') else \
                               urlparse.urljoin(self.root, value.get('href'))
                    value = self.parse_single(href)

                    if type(value) == dict or type(value) == list:
                        data[key][attr] = value
                        self.traverse_json(data[key][attr], to_type)

                    else:
                        cls = type(value).__name__.lower()
                        if cls == 'unicode' or cls == 'nonetype':
                            cls = 'str'
                        data[key][attr] = cls

                else: # Check for existence of array
                    if '[]' in attr: # Key actually refers to array(s)
                        # Empty key in keys specifies array, otherwise dict
                        keys = re.compile(r"(?:\[(\w*?)\])").findall(attr)
                        attr = attr.split('[')[0]
                        obj = data[key]
                        last_key = keys.pop()
                        keys.insert(0, attr)

                        while len(keys) > 0:
                            k = keys.pop(0)
                            next_key = keys[0] if len(keys) > 0 else None
                            replace = obj.get(k, None)

                            if next_key is not None and len(next_key) == 0:
                                keys.pop(0)
                                if type(replace) != list:
                                    obj[k] = [{}]
                                obj = obj[k][0]
                            else:
                                if type(replace) != dict:
                                    obj[k] = {}
                                obj = obj[k]

                        if to_type:
                            obj[last_key] = self.get_type(value.text)
                        else:
                            obj[last_key] = value.text
                    else:
                        if to_type:
                            data[key][attr] = self.get_type(value.text)
                        else:
                            data[key][attr] = value.text

        return data


class BitbucketScraper(BaseScraper):
    """
    TODO: Write this.
    """
    pass
