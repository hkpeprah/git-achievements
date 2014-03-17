import json

from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
from django.template import RequestContext, loader
from django.shortcuts import render, render_to_response, redirect



def index_view(request):
    """
    Project index page.  Mostly a splash page that users arrive at when they reach
    the application page.

    @param request: Djagno request object
    @return: HttpResponse
    """
    conf = settings.BASIC_EXAMPLE_CONFIG

    return render_to_response('achievement/index.html', 
        context_instance=RequestContext(request, {
            'contributors': settings.CONTRIBUTORS,
            'carousel': settings.CAROUSEL,
            'titles': conf['titles']
        })
    )


def login_view(request):
    """
    Login page for the application.  This might actually just end up being a wrapper
    for Github/Bitbucket authentication, but for the time being it will be a page
    where they can OAuth.

    @param request: Django request object
    @return: HttpResponse
    """
    return render_to_response('achievement/login.html',
        context_instance=RequestContext(request))


def leaderboard_view(request):
    """
    Doesn't require authentication.  Lists the users in decreasing order of score
    (based on achievements) by default, otherwise, uses the query parameters passed
    by a search/filter to order the users and render the view.

    @param request: Django request object
    @return: HttpResponse
    """
    examples = {}
    examples['users'] = settings.CONTRIBUTORS
    examples['achievements'] = settings.ACHIEVEMENTS

    return render_to_response('achievement/leaderboard.html',
        context_instance=RequestContext(request, {
            'examples': examples
        })
    )
