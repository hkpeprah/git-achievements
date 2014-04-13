import json
import random

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.exceptions import ValidationError
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, render_to_response, redirect, get_object_or_404

from app.services.models import Event
from app.services.utils import get_contributors, json_response
from app.achievement.models import (Achievement, Condition, Badge, UserProfile, ValueCondition, AttributeCondition,
                                    CustomCondition, AchievementCondition, Difficulty, AchievementType, Method, ConditionType)


@require_http_methods(["GET"])
def index_view(request):
    """
    Project index page.  Mostly a splash page that users arrive at when they reach
    the application page.

    @param request: Djagno request object
    @return: HttpResponse
    """
    top_achievers = UserProfile.objects.all().order_by('-points')[:10]

    return render_to_response('achievement/index.html', 
        context_instance=RequestContext(request, {
            'achievers': top_achievers
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
    Returns the page for creating an achievement on GET, otherwise creates the
    achievement and redirects on POST.

    @param request: HttpRequest object
    @return: HttpResponse
    """
    if request.method == 'POST' and request.is_ajax():
        # Validate the Form Data
        data = json.loads(request.body)
        achievement = data['achievement']
        badge = data.get('badge', None)
        conditions = []

        try:
            difficulty = Difficulty.objects.get(pk=achievement['difficulty'])
            achievement_type = AchievementType.objects.get(pk=achievement['type'])
            achievement = Achievement(name=achievement['name'], description=achievement['description'], difficulty=difficulty,
                achievement_type=achievement_type, grouping=achievement['grouping'])

            achievement.full_clean()
            if badge:
                badge = Badge(name=badge['name'], description=badge['description'])
                badge.full_clean()

            achievement.badge = badge

            for condition in data.get('valueconditions', []):
                method = Method.objects.get(pk=condition['method'])
                event = Event.objects.get(pk=condition['event_type'])
                condition = ValueCondition(description=condition['description'], attribute=condition['attribute'],
                    value=condition['value'], method=method, condition_type=ConditionType.objects.get(pk=1),
                    event_type=event)
                condition.full_clean()
                conditions.append(condition)

            for condition in data.get('customconditions', []):
                condition = CustomCondition.objects.get(pk=condition['id'])
                conditions.append(condition)

            if len(conditions) == 0:
                raise ValidationError("Atleast one condition must be added for the achievement.")

        except (ValidationError, CustomCondition.DoesNotExist, Difficulty.DoesNotExist, Event.DoesNotExist,
                Method.DoesNotExist, AchievementType.DoesNotExist) as e:
            print e
            if isinstance(e, ValidationError):
                # ValidationError returns multiple messages
                e = ', '.join(e.messages)

            return json_response({
                'msg': str(e)
            }, False)

        if badge:
            badge.save()

        achievement.save()
        for condition in conditions:
            condition.save()
            achievement_condition = AchievementCondition(content_object=condition)
            achievement_condition.save()
            achievement_condition.achievements.add(achievement)
            achievement_condition.save()

        return json_response({})

    return render_to_response('achievement/achievements/create.html',
        context_instance=RequestContext(request))


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
        # Vote on the achievement provided the user can vote.
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
    achievement = get_object_or_404(Achievement, pk=achievement_id, active=True)
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
    achievements = Achievement.objects.filter(active=True)

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
def view_own_profile(request):
    """
    Views the user's own profile.  Doesn't require a username parameter as
    we get the user from the request.user object.

    @param request: HttpRequest object
    @return HttpResponse
    """
    if request.user.is_authenticated():
        username = request.user.username
        return view_profile(request, username)
    return redirect('/users')


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
        context_instance=RequestContext(request, {
            'contributors': get_contributors(),
        })
    )
