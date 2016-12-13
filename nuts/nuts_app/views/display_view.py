from django.shortcuts import render, get_object_or_404

from django.http import Http404

# decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required
from nuts_app.models import *
import datetime

from django.db import transaction

from django.views.decorators.csrf import ensure_csrf_cookie
from nuts_app.forms import *
from django.core import serializers
from django.http import JsonResponse, HttpResponse

@ensure_csrf_cookie # Gives CSRF token for later requests.
@login_required
def display_home(request):
    context = {'username': request.user.username, 'id': request.user.id}
    return render(request, 'nuts/home.html', context)

@login_required
def global_plans(request):

    context = {'username': request.user.username}
    now = datetime.datetime.now()
    nuts = sorted(Nut.objects.filter(privilege = 'Public').exclude(state='DONE').filter(expire_time__gte=now), key=post_key, reverse=True)
    context['nuts'] = nuts

    # new
    # append all the comment for each nut
    nut_id_set = set()
    for nut in nuts:
        nut_id_set.add(nut.id)
    allcomments = Comment.objects.all().order_by("timestamp")
    comments = []
    for comment in allcomments:
        if comment.nut.id in nut_id_set:
            comments.append(comment)
    context["comments"] = comments

    # bw: like plans, get all the user's liked plan id
    squirrel = get_object_or_404(Squirrel, user = request.user)
    like_nuts = squirrel.like_plan

    like_nut_ids = []
    for like_nut in like_nuts.all():
        like_nut_ids.append(like_nut.id)
    context["like_nut_ids"] = like_nut_ids

    return render(request, 'nuts/global_plans.html', context)

def post_key(nut):
    return nut.timestamp

@login_required
def get_all_public(request):
    context = {'username': request.user.username}
    now = datetime.datetime.now()
    nuts = sorted(Nut.objects.filter(privilege = 'Public').exclude(state='DONE').filter(expire_time__gte=now), key=post_key, reverse=True)
    nutsJ = []
    for nut in nuts:

        description = nut.description.replace('\n', ' ').replace('\r', '')
        nutJ = {'author': nut.author.username,
                 'timestamp': nut.timestamp,
                 'title': nut.title,
                 'description' : description,
                 'expire_time': nut.expire_time,
                 'expires': False,
                 'id': nut.id,
                 'like_num': nut.liked_user.count,
                 'user_id': nut.author.id}
        nutsJ.append(nutJ)

    # new
    # append all the comment for each nut
    nut_id_set = set()
    for nut in nutsJ:
        nut_id_set.add(nut['id'])
    allcomments = Comment.objects.all().order_by("timestamp")
    comments = []
    for comment in allcomments:
        if comment.nut.id in nut_id_set:
            comments.append(comment)
    context["comments"] = comments
    
    context['nuts'] = nutsJ


    # bw: get current user's like plans' ids
    user_like_plan_ids = []
    squirrel = get_object_or_404(Squirrel, user = request.user)
    like_plans = squirrel.like_plan
    for like_plan in like_plans.all():
        user_like_plan_ids.append(like_plan.id)
    context["user_like_plan_ids"] = user_like_plan_ids


    #print(render(request, 'json/nuts_with_comments.json', context, content_type='application/json'))
    return render(request, 'json/nuts_with_comments.json', context, content_type='application/json')

@login_required
def get_all_eat(request):
    context = {'username': request.user.username}
    now = datetime.datetime.now()
    squirrel = get_object_or_404(Squirrel, user = request.user)
    nuts = sorted(squirrel.follow_plan.all(), key=post_key, reverse=True)
    nutsJ = []
    for nut in nuts:
        nutJ = {'author': nut.author.username,
                 'timestamp': nut.timestamp,
                 'title': nut.title,
                 'description' : nut.description,
                 'expire_time': nut.expire_time,
                 'id': nut.id,
                 'like_num': nut.liked_user.count,
                 'user_id': nut.author.id}
        if(now.date() > nut.expire_time):
            nutJ['expires'] = True
        else:
            nutJ['expires'] = False
        nutsJ.append(nutJ)
    
    # new
    # append all the comment for each nut
    nut_id_set = set()
    for nut in nutsJ:
        nut_id_set.add(nut['id'])
    allcomments = Comment.objects.all().order_by("timestamp")
    comments = []
    for comment in allcomments:
        if comment.nut.id in nut_id_set:
            comments.append(comment)
    context["comments"] = comments

    # bw: get current user's like plans' ids
    user_like_plan_ids = []
    squirrel = get_object_or_404(Squirrel, user = request.user)
    like_plans = squirrel.like_plan
    for like_plan in like_plans.all():
        user_like_plan_ids.append(like_plan.id)
    context["user_like_plan_ids"] = user_like_plan_ids

    context['nuts'] = nutsJ
    return render(request, 'json/nuts_with_comments.json', context, content_type='application/json')

@login_required
def get_all_follow(request):
    context = {'username': request.user.username}
    now = datetime.datetime.now()
    squirrel = get_object_or_404(Squirrel, user = request.user)
    nuts = []
    squirrel_fol = squirrel.follow_user.all()
    for s in squirrel_fol:
        nuts.extend(s.user.nut_set.filter(privilege = 'Public'))
    nuts = sorted(nuts, key=post_key, reverse=True)
    nutsJ = []
    for nut in nuts:
        nutJ = {'author': nut.author.username,
                 'timestamp': nut.timestamp,
                 'title': nut.title,
                 'description' : nut.description,
                 'expire_time': nut.expire_time,
                 'id': nut.id,
                 'like_num': nut.liked_user.count,
                 'user_id': nut.author.id}
        if(now.date() > nut.expire_time):
            nutJ['expires'] = True
        else:
            nutJ['expires'] = False
        nutsJ.append(nutJ)

    # new
    # append all the comment for each nut
    nut_id_set = set()
    for nut in nutsJ:
        nut_id_set.add(nut['id'])
    allcomments = Comment.objects.all().order_by("timestamp")
    comments = []
    for comment in allcomments:
        if comment.nut.id in nut_id_set:
            comments.append(comment)
    context["comments"] = comments

    # bw: get current user's like plans' ids
    user_like_plan_ids = []
    squirrel = get_object_or_404(Squirrel, user = request.user)
    like_plans = squirrel.like_plan
    for like_plan in like_plans.all():
        user_like_plan_ids.append(like_plan.id)
    context["user_like_plan_ids"] = user_like_plan_ids
    
    context['nuts'] = nutsJ
    return render(request, 'json/nuts_with_comments.json', context, content_type='application/json')

@login_required
@transaction.atomic
def add_comment(request):

    message = []

    if request.method == "GET":
        comment = {"message" : "No new comment posted."}
        return render(request, 'json/comment.json', context, content_type='application/json')

    form = CommentForm(request.POST)
    if not form.is_valid():
        raise Http404
    else:
        nut = Nut.objects.get(id=request.POST["nut_id"])
        new_comment = Comment(text=request.POST["comment"], nut=nut, user=request.user)
        new_comment.save()
        message.append("Successfully add a comment.")

        timestamp = new_comment.timestamp
        user = request.user

        comment = {"text": request.POST["comment"], "nut_id":request.POST["nut_id"], "user_id":user.id, "user":{"username":user.username}, "timestamp":timestamp}
        comment["message"] = message
        context = {"comment":comment}

        return render(request, 'json/comment.json', context, content_type='application/json')

@login_required
def get_message(request):
    form = RoomIdForm(request.GET)
    if form.is_valid():
        message = Message.objects.filter(room_id=form.cleaned_data['room_id'])
        message = sorted(message, key=message_key)[-10:]
        json_msg = serializers.serialize('json', message)
        return JsonResponse(json_msg, safe=False)
    return HttpResponse()

def message_key(msg):
    return msg.timestamp
