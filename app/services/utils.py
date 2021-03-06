import json
import urllib2

import ipaddress
from django.conf import settings
from django.http import HttpResponse

from app.services.models import Event


def initialize_webhook_addresses():
    """
    Adds the webhook addresses to the settings variable.
    """
    if not hasattr(settings, 'GITHUB_IP_ADDRESSES'):
        blocks = get_api_data('https://api.github.com/meta')
        blocks = blocks['hooks']
        addresses = []
        for block in blocks:
            addresses += map(lambda ip: str(ip), list(ipaddress.ip_network(block).hosts()))
        setattr(settings, 'GITHUB_IP_ADDRESSES', addresses)

    return None


def get_client_ip(request):
    """
    Gets the client's ip address from a request object.
    """
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', None)
    real_ip = request.META.get('HTTP_X_REAL_IP', None)
    if forwarded_for:
        return forwarded_for.split(',')[0]
    elif real_ip:
        return real_ip
    return request.META.get('REMOTE_ADDR')


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
    except (urllib2.HTTPError, urllib2.URLError):
        pass
    return None


def get_contributors():
    """
    Gets a list of the contributors to the Github project.

    @return: list
    """
    if hasattr(settings, "PROJECT_CONTRIBUTORS"):
        return settings.PROJECT_CONTRIBUTORS

    contributors_list = get_api_data(settings.CONTRIBUTORS_URL)
    contributors_list = [] if contributors_list is None else contributors_list
    contributors = []

    for contributor in contributors_list:
        contributor = get_api_data(contributor['url'])
        if contributor is not None:
            contributors.append(contributor)

    setattr(settings, "PROJECT_CONTRIBUTORS", contributors)
    return contributors


def json_response(data, success=True):
    """
    Creates a HttpResponse for returning json data.

    @param data: Object
    @return: HttpResponse
    """
    return HttpResponse(json.dumps({
            'response': data,
            'success': success
        }, separators=(',', ':'), indent=4),
        content_type="application/json", status=200)
