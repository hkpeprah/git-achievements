import json
import random

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, render_to_response, redirect, get_object_or_404

from app.assets.models import Achievement, Condition, Badge, UserProfile


@require_http_methods(["GET"])
def index_view(request):
    """
    Project index page.  Mostly a splash page that users arrive at when they reach
    the application page.

    @param request: Djagno request object
    @return: HttpResponse
    """
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


@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Login page for the application.  This might actually just end up being a wrapper
    for Github/Bitbucket authentication, but for the time being it will be a page
    where they can OAuth.

    @param request: Django request object
    @return: HttpResponse
    """
    if request.user.is_authenticated():
        # If the user is logged in, log them out
        auth_logout(request)

    # User is not authenticated here, so display the login
    # page for them to authenticate
    return render_to_response('achievement/login.html',
        context_instance=RequestContext(request))


@login_required
@require_http_methods(["GET", "POST"])
def create_achievement(request):
    """
    Returns the page with the form for creating an achievement.

    @param request: HttpRequest object
    @return: HttpResponse
    """
    return HttpResponse("Create achievement.")


@login_required
@require_http_methods(["GET", "POST"])
def approve_achievement(request, achievement_id):
    """
    Generates the page for approving/voting on achievements.  Moderators can
    accept/reject an achievement or attach notes, while non-moderators can
    attach notes and vote.

    @param request: HttpRequest object
    @param achievement_id: The id of the achievement to vote on
    @return: HttpResponse
    """
    achievement = None
    if achievement_id is None:
        achievement = Achievement.objects.filter(active=False)
        achievement = achievement[0] if len(achievement) > 0 else None
    else:
        achievement = get_object_or_404(Achievement, pk=achievement_id)

    if request.method == "POST":
        # Vote on the achievement provided the user can
        # vote.
        pass

    if achievement is None:
        return render_to_response('achievement/achievements/no_vote.html',
            context_instance=RequestContext(request))

    return render_to_response('achievement/achievements/approve.html',
        context_instance=RequestContext(request, {
            'achievement': achievement
        })
    )


@login_required
@require_http_methods(["GET", "POST"])
def edit_achievement(request, achievement_id):
    """
    Page where creators and moderators can edit achievements.  Creators can only
    edit non-active achievements.

    @param request: HttpRequest object
    @param achievement_id: The id of the achievement to edit
    @return: HttpResponse object
    """
    return HttpResponse("Achievement edit page.")


@require_http_methods(["GET"])
def view_achievement(request, achievement_id):
    """
    Doesn't require authentication, but returns the page for viewiing an achievement,
    and the information relevant to that achievement.

    @param request: HttpRequest object
    @param achievement_id: The id of the achievement to view
    @return: HttpResponse object
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


@require_http_methods(["GET"])
def view_achievements(request):
    """
    Doesn't require authentications.  List all the achievements in the application
    via pagination.

    @param request: HttpRequest object
    @return HttpResponse
    """
    achievements = Achievement.objects.all()

    return render_to_response('achievement/achievements/all.html',
        context_instance=RequestContext(request, {
            'achievements': achievements
        })
    )


@require_http_methods(["GET"])
def view_profile(request, username):
    """
    Returns the profile for the specified user.  Since usernames are unique,
    we are able to query by them.

    @param request: HttpRequest object
    @param username: Username of the user (a string)
    @return: HttpResponse
    """
    user = get_object_or_404(User, username=username)

    return render_to_response('achievement/users/profile.html',
        context_instance=RequestContext(request, {
            'profile': user.profile
        })
    )


@require_http_methods(["GET"])
def view_profiles(request):
    """
    Doesn't require authentication.  Lists the users in decreasing order of score
    (based on achievements) by default, otherwise, uses the query parameters passed
    by a search/filter to order the users and render the view.

    @param request: HttpRequest object
    @return: HttpResponse
    """
    users = UserProfile.objects.all()

    return render_to_response('achievement/users/all.html',
        context_instance=RequestContext(request, {
            'users': users
        })
    )


@require_http_methods(["GET"])
def faq(request):
    """
    Displays the faq/about page for the project.
    """
    return render_to_response("achievement/about/faq.html",
        context_instance=RequestContext(request))
