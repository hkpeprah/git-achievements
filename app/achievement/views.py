import json
import random

from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
from django.template import RequestContext, loader
from django.shortcuts import render, render_to_response, redirect, get_object_or_404

from app.assets.models import Achievement, Condition, Badge, UserProfile


def index_view(request):
    """
    Project index page.  Mostly a splash page that users arrive at when they reach
    the application page.

    @param request: Djagno request object
    @return: HttpResponse
    """
    conf = settings.BASIC_EXAMPLE_CONFIG
    badges = sorted(Badge.objects.all().order_by('pk'),
                    key = lambda x: random.random())

    if len(badges) == 0:
        badges = conf['badges']

    return render_to_response('achievement/index.html', 
        context_instance=RequestContext(request, {
            'contributors': settings.CONTRIBUTORS,
            'carousel': settings.CAROUSEL,
            'badges': badges[:5]
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
    examples = {
        'users': settings.CONTRIBUTORS,
        'achievements': settings.ACHIEVEMENTS
    }

    # Collect and filter the DB data
    achievements = Achievement.objects.all()

    return render_to_response('achievement/leaderboard.html',
        context_instance=RequestContext(request, {
            'examples': examples,
            'achievements': achievements
        })
    )

def create_achievement(request):
    """
    """
    pass


def approve_achievement(request, achievement_id):
    """
    """
    pass


def edit_achievement(request, achievement_id):
    """
    """
    pass


def view_achievement(request, achievement_id):
    """
    Doesn't require authentication, but returns the page for viewiing an achievement,
    and the information relevant to that achievement.
    """
    achievement = get_object_or_404(Achievement, pk=achievement_id)
    conditions = list(genericcondition.condition.description for genericcondition in \
        achievement.conditions.all())

    return render_to_response('achievement/achievements/view.html',
        context_instance=RequestContext(request, {
            'achievement': achievement,
            'unsatisfied_conditions': conditions,
            'satisfied_conditions': []
        })
    )


def view_profile(request, user_id):
    """
    """
    pass
