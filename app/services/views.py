import json

import re
from django.conf import settings
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test, login_required

from app.services.models import Event
from app.services.hooks import GithubHook
from app.achievement.hooks import check_for_unlocked_achievements
from app.services.utils import json_response, initialize_webhook_addresses, get_client_ip


@login_required
@require_http_methods(['GET'])
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


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def web_hook(request):
    """
    Processes a Web Hook service request.

    @param request: HttpRequest
    @return: HttpResponse
    """
    if request.method == "GET":
        return HttpResponse("Hello World!", status=200)

    headers, request_address = request.META, get_client_ip(request)
    response = json_response({})

    # Initialize web hook addresses if not already
    initialize_webhook_addresses()
    if request_address in settings.GITHUB_IP_ADDRESSES:
        if settings.DEBUG:
            print "Received webhook event from: %s" % request_address
        event = headers.get('HTTP_X_GITHUB_EVENT', '')
        payload = request.POST.get('payload', None)
        if not payload:
            payload = json.loads(request.body)
        response = GithubHook.process_event(event, payload)

    return response


@csrf_exempt
@require_http_methods(['POST'])
def web_local_hook(request):
    """
    Processes a request from a local web service request.

    @param: HttpRequest
    @return: HttpResponse
    """
    data = json.loads(request.body)
    data = check_for_unlocked_achievements(data.get('event'), data.get('payload'))

    return HttpResponse(json.dumps(data), status=200,
        content_type="application/json")
