from django.conf import settings

from app.services.models import Event
from app.services.scrapers import GithubScraper, BitbucketScraper


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
