import json
import urllib
import urllib2


class GoogleSearch(object):
    """
    Wrapper for Google Search using Google's Ajax API and search service.
    Add apis as they become available or not.

    @deprecated: Google's Ajax API is deprecated and should be phased out.
    """
    base_url = 'http://ajax.googleapis.com/ajax/services/search'
    version = '1.0'
    apis = [
        'web',
        'images'
    ]

    def __init__(self, method=None):
        """
        Intializes the Search APi by setting the endpoints for the various supported
        apis.

        @param self: GoogleSearch instance
        @param method: Initial endpoint to call
        @return: GoogleSearch instance
        """
        self.url = self.base_url

        for api in self.apis:
            setattr(self, api, self.make_api(api))

        if method is not None:
            return self[method]()

    def make_api(self, endpoint):
        """
        Adds an endpoint to the API.

        @param endpoint: String endpoint
        @return: function
        """
        def api(queries):
            """
            Wraps the API request.
            """
            self.url += "/{0}?".format(endpoint)
            self.add_querystrings(queries)

            return self
        return api

    def get(self):
        """
        Opens the passed google api url and makes a request; coerces the returned data to a json
        object and returns the list of results.

        @param self: GoogleSearch instance
        @param url: The url to request
        @return: Tuple
        """
        response = urllib.urlopen(self.url) # TODO: Error check this
        self.url = self.base_url # Reset url
        data = response.read()
        data = json.loads(data)
        # Get the results from the json object

        try:
            results = data['responseData']['results']
            cls = results[0].get('GsearchResultClass', None) if len(results) \
                      else None
        except TypeError:
            return [], None

        return results, cls

    def add_querystrings(self, queries={}):
        """
        Adds a querystring or multiple key, value paries to the url.

        @param queries: Dict or string
        @return: GoogleSearch instance
        """
        if not type(queries) == dict:
            try:
                tmp = {}
                tmp['q'] = str(queries)
                queries = tmp
            except ValueError:
                raise ValueError("Expected dict or string, given %s" % type(queries))

        queries['v'] = self.version
        querystring = urllib.urlencode(queries)
        self.url += querystring

        return self


class GoogleResponseDataFormatter(object):
    """
    Formats and filters the response data from a GoogleSearch result set.
    """
    available_fields = []

    @classmethod
    def __call__(cls, data):
        """
        Calls the formatter and returns the formatted data.

        @param cls: The formatter instance
        @param data: The json data to format
        @return: json
        """
        filtered = data

        if len(cls.available_fields) > 0:
            filtered = []

            for d in data: # Filter the keys in the objects
                fields = {}
                for key in filter(lambda x: x in cls.available_fields, d.keys()):
                    filter_key = key.replace("NoFormatting", "")
                    fields[filter_key] = d[key]
                filtered.append(fields)

        return filtered


class GoogleImageSearchFormatter(GoogleResponseDataFormatter):
    available_fields = [
        'titleNoFormatting',
        'contentNoFormatting',
        'url',
        'height',
        'width'
    ]


class GoogleWebSearchFormatter(GoogleResponseDataFormatter):
    available_fields = [
        'titleNoFormatting',
        'content',
        'url'
    ]
