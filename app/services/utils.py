import json
import urllib2
from django.conf import settings
from django.http import HttpResponse

from app.services.models import Event
from app.services.scrapers import GithubScraper, BitbucketScraper


def get_api_data(url, headers=None):
    """
    Makes a request to the specified API for data, defaults to getting
    json data.

    @param url: String, the url to make the request to
    @param headers: Dictionary of headers
    @return: dict
    """
    if headers is None:
        headers = {"Content-type": "application/json"}

    try:
        req = urllib2.urlopen(url)
        return json.loads(req.read())
    except (urllib2.HTTPError, urllib2.URLError) as e:
        pass
    return None


def refresh_event_json():
    """
    Refreshes the json for the supported scrapers by refreshing
    the event models.  Creates a new object unless the object already
    exists in the DB, otherwise it updates.

    @return: None
    """
    services = getattr(settings, "HOSTING_API_SERVICES", (
            'Github',
        )
    )

    for service in services:
        scraper = None

        if service == "Github":
            scraper = GithubScraper()
        else:
            continue

        payload = scraper.parse()
        types = scraper.parse(to_type=True)

        for ev_type, data in payload.iteritems():
            ev, created = Event.objects.get_or_create(name=ev_type, service=service)
            ev.payload = data
            ev.attributes = types.get(ev_type, {})
            ev.save()

    return None


def get_contributors():
    """
    Gets a list of the contributors to the Github project.

    @return: list
    """
    contributors_list = get_api_data("https://api.github.com/orgs/git-achievements/public_members")
    contributors_list = [] if contributors_list is None else contributors_list
    contributors = []

    for contributor in contributors_list:
        contributor = get_api_data(contributor['url'])
        if contributor is not None:
            contributors.append(contributor)

    return contributors


def json_response(data):
    """
    Creates a HttpResponse for returning json data.

    @param data: Object
    @return: HttpResponse
    """
    return HttpResponse(json.dumps({
            'response': data,
            'success': True
        }, separators=(',', ':'), indent=4),
        content_type="application/json", status=200)
