import re
import json

from django.contrib import messages
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import user_passes_test, login_required

from app.services.models import Event


@login_required
@user_passes_test(lambda u: u.is_superuser)
def service_events(request, service):
    """
    Renders a page displaying the various supported events and payloads
    for the the specified service.

    @param request: HttpRequest object
    @param service: String, the name of the service of whose events to grab
    @return: HttpResponse
    """
    events = [event for event in Event.objects.filter(service=service.title())]

    for index, event in enumerate(events[:]):
        name = event.name
        title = ''.join(substr.title() for substr in re.split('[_\-]', event.name))
        event = json.dumps(event.payload, indent=4,
            separators=(",", ":"))

        events[index] = {
            'name': name,
            'title': title,
            'payload': event.lstrip().rstrip()
        }

    return render_to_response("services/events/index.html",
        context_instance=RequestContext(request, {
            'service': service.title(),
            'events': events
        })
    )
