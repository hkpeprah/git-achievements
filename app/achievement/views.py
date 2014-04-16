import json
import urllib2

from django.db.models import Q
from django.conf import settings
from django.utils.html import escape
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response, redirect, get_object_or_404

from app.services.models import Event
from app.services.utils import get_contributors, json_response
from app.achievement.models import (Achievement, Badge, UserProfile, ValueCondition,
                                    CustomCondition, AchievementCondition,
                                    Difficulty, AchievementType, Method, ConditionType)


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
            achievement = Achievement(name=escape(achievement['name']), description=escape(achievement['description']),
                difficulty=difficulty, achievement_type=achievement_type, grouping=achievement['grouping'])

            achievement.full_clean()
            if badge:
                badge = Badge(name=escape(badge['name']), description=escape(badge['description']))
                badge.full_clean()

            achievement.badge = badge

            for condition in data.get('valueconditions', []):
                method = Method.objects.get(pk=condition['method'])
                event = Event.objects.get(pk=condition['event_type'])
                condition = ValueCondition(description=escape(condition['description']), attribute=condition['attribute'],
                    value=condition['value'], method=method, condition_type=ConditionType.objects.get(pk=1),
                    event_type=event)
                condition.full_clean()
                conditions.append(condition)

            for condition in data.get('customconditions', []):
                condition = CustomCondition.objects.get(pk=condition['id'])
                conditions.append(condition)

            if len(conditions) == 0:
                raise ValidationError("Atleast one condition must be added for the achievement.")

        except (ObjectDoesNotExist, ValidationError) as e:
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
    if request.method == "POST" and achievement_id:
        # Vote on the achievement provided the user can vote, or approve
        # the achievement provided the user is a moderator/admin
        achievement = get_object_or_404(Achievement, pk=achievement_id, active=False)
        profile = request.user.profile
        threshold = settings.ACHIEVEMENT_APPROVAL_THRESHOLD
        vote = request.POST.get('vote')

        if vote == "upvote":
            if profile in achievement.downvoters.all():
                achievement.downvoters.remove(profile)
            else:
                achievement.upvoters.add(profile)
            # If we've reached or passed the threshold, the achievement can be
            # added as active
            if achievement.approval >= threshold and threshold > 0:
                achievement.active = True
                achievement_id = None

        elif vote == "downvote":
            if profile in achievement.upvoters.all():
                achievement.upvoters.remove(profile)
            else:
                achievement.downvoters.add(profile)

        elif vote == "approved" and (request.user.is_superuser or profile.moderator):
            achievement.active = True
            achievement_id = None

        achievement.save()

        if achievement_id:
            return redirect('approve_achievement', achievement_id=achievement_id)
        return redirect('approve_achievement')

    achievement = None
    achievements = Achievement.objects.filter(active=False)
    if not achievement_id:
        achievement = achievements[0] if len(achievements) > 0 else None
    else:
        achievement = get_object_or_404(Achievement, pk=achievement_id)

    # Find the index of the curreent achievement in the achievements list
    index = 0
    for i, item in enumerate(achievements):
        if item == achievement:
            index = i
            break

    # Paginate by finding the next and previous achievements
    prev_page = None if index == 0 else achievements[index - 1].pk
    next_page = None if index == len(achievements) - 1 else achievements[index + 1].pk
    conditions = list(condition.condition for condition in achievement.conditions.all())

    if achievement is None:
        return render_to_response('achievement/achievements/no_vote.html',
            context_instance=RequestContext(request))

    return render_to_response('achievement/achievements/approve.html',
        context_instance=RequestContext(request, {
            'achievement': achievement,
            'conditions': conditions,
            'next_page': next_page,
            'prev_page': prev_page
        }))


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
    query = urllib2.unquote(request.GET.get('q', ""))
    page = request.GET.get('page', 1)
    achievements = Achievement.objects.filter(Q(active=True) &
                                              (Q(name__contains=query) | Q(difficulty__name__contains=query)))
    paginator = Paginator(achievements, 15)

    try:
        achievements = paginator.page(page)
    except PageNotAnInteger:
        # If the page isn't an integer, just return the first page
        achievements = paginator.page(1)
    except EmptyPage:
        # Page is out of range (> # of pages), so deliver last page
        achievements = paginator.page(paginator.num_pages)

    return render_to_response('achievement/achievements/all.html',
        context_instance=RequestContext(request, {
            'achievements': achievements,
            'q': query
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
    query = urllib2.unquote(request.GET.get("q", ""))
    page = request.GET.get('page', 1)
    users = UserProfile.objects.filter(user__username__contains=query)
    paginator = Paginator(users, 15)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render_to_response('achievement/users/all.html',
        context_instance=RequestContext(request, {
            'users': users,
            'q': query
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
