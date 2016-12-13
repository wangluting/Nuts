from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.urls import reverse
from django.http import Http404, HttpResponse
from django.db import transaction
from django.contrib.auth.models import User
from nuts_app.forms import *
from nuts_app.models import *
from datetime import timedelta
from collections import OrderedDict
from dateutil.parser import parse as parse_date
import re


@transaction.atomic
@login_required
def create_plan(request):
    context = {}
    context['username'] = request.user.username
    if request.method == 'GET':
        context['form'] = PlanForm()
        return render(request, 'nuts/create_plan.html', context)

    form = PlanForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'nuts/create_plan.html', context)

    lat = request.POST.get('lat')
    lng = request.POST.get('lng')

    if(form.cleaned_data['expire_same']):
        if(lat and lng):
            new_nut = Nut(author=request.user,
                  start_time=form.cleaned_data['start_time'],
                  expire_time=form.cleaned_data['start_time'],
                  title=form.cleaned_data['title'],
                  description=form.cleaned_data['description'],
                  privilege=form.cleaned_data['privilege'],
                  lat = float(lat),
                  lng = float(lng))
        else:
            new_nut = Nut(author=request.user,
                  start_time=form.cleaned_data['start_time'],
                  expire_time=form.cleaned_data['start_time'],
                  title=form.cleaned_data['title'],
                  description=form.cleaned_data['description'],
                  privilege=form.cleaned_data['privilege'])
    else:
        if (lat and lng):
            new_nut = Nut(author=request.user,
                  start_time=form.cleaned_data['start_time'],
                  expire_time=form.cleaned_data['expire_time'],
                  title=form.cleaned_data['title'],
                  description=form.cleaned_data['description'],
                  privilege=form.cleaned_data['privilege'],
                  lat = float(lat),
                  lng = float(lng))
        else:
            new_nut = Nut(author=request.user,
                  start_time=form.cleaned_data['start_time'],
                  expire_time=form.cleaned_data['expire_time'],
                  title=form.cleaned_data['title'],
                  description=form.cleaned_data['description'],
                  privilege=form.cleaned_data['privilege'])
    new_nut.save()

    return redirect('/nuts/')

@transaction.atomic
@login_required
def create_range_plan(request):
    form = TimeRangeForm(request.POST)
    context = {}
    context['username'] = request.user.username
    if form.is_valid():
        s = datetime.datetime.fromtimestamp(float(form.cleaned_data['start'])/1000.0)
        e = datetime.datetime.fromtimestamp(float(form.cleaned_data['end'])/1000.0) - timedelta(days=1)
        context['form'] = PlanForm(initial = {'start_time': s,
                                            'expire_time': e,
                                            'expire_same': False})
        print(s)
        return render(request, 'nuts/create_plan.html', context)

    form = PlanForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'nuts/create_plan.html', context)

    if(form.cleaned_data['expire_same']):

            new_nut = Nut(author=request.user,
                  start_time=form.cleaned_data['start_time'],
                  expire_time=form.cleaned_data['start_time'],
                  title=form.cleaned_data['title'],
                  description=form.cleaned_data['description'],
                  privilege=form.cleaned_data['privilege'])

    else:
        new_nut = Nut(author=request.user,
                  start_time=form.cleaned_data['start_time'],
                  expire_time=form.cleaned_data['expire_time'],
                  title=form.cleaned_data['title'],
                  description=form.cleaned_data['description'],
                  privilege=form.cleaned_data['privilege'])

    new_nut.save()
    return redirect('/nuts/')

@login_required
def get_todo_plan(request):
    nuts = Nut.get_todo(user=request.user)
    context = {"nuts": nuts}
    return render(request, 'json/nuts.json', context, content_type='application/json')

@login_required
def get_doing_plan(request):
    nuts = Nut.get_doing(user=request.user)
    context = {"nuts": nuts}
    return render(request, 'json/nuts.json', context, content_type='application/json')

@login_required
def get_done_plan(request):
    nuts = Nut.get_done(user=request.user)
    context = {"nuts": nuts}
    return render(request, 'json/nuts.json', context, content_type='application/json')

@login_required
def my_plan(request):
    context = {'username': request.user.username}
    return render(request, 'nuts/view_all_plan.html', context)

@login_required
def view_all_plan(request):

    nuts = Nut.get_all(user=request.user)
    context = {"nuts": nuts}
    context['username'] = request.user.username
    return render(request, 'json/nuts.json', context, content_type='application/json')

@login_required
def view_all_mine(request):
    nuts = Nut.get_all(user=request.user).exclude(state='DONE')
    nutsJ = []
    for nut in nuts:
        nutJ = {'id': nut.id,
                 'title': nut.title,
                 'start' : nut.start_time,
                 'end': nut.expire_time+timedelta(days=1)}
        if(nut.state == 'TODO'):
            nutJ['color'] = 'rosybrown'
        nutsJ.append(nutJ)
    
    squirrel = get_object_or_404(Squirrel, user = request.user)
    now = datetime.datetime.now()
    nuts = squirrel.follow_plan.all().filter(expire_time__gte=now)
    for nut in nuts:
        nutJ = {'id': nut.id,
                 'title': nut.title,
                 'start' : nut.start_time,
                 'end': nut.expire_time+timedelta(days=1)}
        nutJ['color'] = 'LightSeaGreen'
        nutsJ.append(nutJ)

    context = {"nuts": nutsJ}
    context['username'] = request.user.username
    return render(request, 'json/calendar_event.json', context, content_type='application/json')

@login_required
def view_plan(request, id):
    try:
        nut = Nut.objects.get(id=id)
    except ObjectDoesNotExist:
        raise Http404("Nut does not exist")
    author = nut.author
    if author != request.user and nut.privilege == 'Private':
        raise Http404("You do not have access to this nut")

    squirrel = Squirrel.objects.get(user=author)
    followers = nut.follow_plan.count()

    context = {'nut': nut, 'squirrel': squirrel, 'followers':followers}
    flag = 1
    if request.user != author:
        flag = 2
        sq_cur = Squirrel.objects.get(user=request.user)
        if nut in sq_cur.follow_plan.all():
            context['eat'] = False
        else:
            context['eat'] = True

    context['flag'] = flag
    context['username'] = request.user.username
    return render(request, 'nuts/view_single_plan.html', context)

@login_required
def update_state(request, id):
    if not 'state' in request.POST or not request.POST['state']:
        raise Http404
    if not 'point' in request.POST or not request.POST['point']:
        raise Http404
    try:
        nut = Nut.objects.get(id=id)
    except ObjectDoesNotExist:
        raise Http404("Nut does not exist")

    state = request.POST['state']
    point = request.POST['point']
    profile = Squirrel.objects.get(user=request.user)
    if nut.state == 'DONE':
        profile.point = profile.point - nut.point
        profile.save()
        nut.point = 0
        nut.save()
    if state == 'DONE':
        profile.point = profile.point + int(point)
        profile.save()
        nut.point = point
        nut.save()
    if (nut.state != state):
        nut.state = state
        nut.save()
    return HttpResponse("")


@transaction.atomic
@login_required
def edit_plan(request, id):
    context = {}
    context['username'] = request.user.username
    try:
        nut = Nut.objects.get(id=id)
    except ObjectDoesNotExist:
        raise Http404("Nut does not exist")

    if request.method == 'GET':
        form = EditPlanForm(instance=nut)
        lat = nut.lat
        lng = nut.lng
        context = {'form':form, 'id':nut.id, 'username': request.user.username, 'lat': lat, 'lng' : lng}
        return render(request, 'nuts/edit_plan.html', context)

    form = EditPlanForm(request.POST, instance=nut)
    context['form'] = form
    context['id'] = id

    if not form.is_valid():
        return render(request, 'nuts/edit_plan.html', context)

    s = request.POST['start_time_year'] + '-' + request.POST['start_time_month'] + '-' + request.POST['start_time_day']
    e = request.POST['expire_time_year'] + '-' + request.POST['expire_time_month'] + '-' + request.POST['expire_time_day']
    if s > e or parse_date(s).date() < datetime.date.today():
        return render(request, 'nuts/edit_plan.html', context)

    nut.start_time = s
    nut.expire_time = e
    nut.lat = float(request.POST.get('lat', 0))
    nut.lng = float(request.POST.get('lng', 0))
    nut.save()
    form.save()

    return redirect('view_plan', id)

@transaction.atomic
@login_required
def edit_plan_time(request):
    form = PlanTimeForm(request.POST)
    if form.is_valid():
        nut = Nut.objects.get(id=form.cleaned_data['id'])
        if nut.author != request.user:
            return HttpResponse()
        s = datetime.datetime.fromtimestamp(float(form.cleaned_data['start'])/1000.0)
        e = datetime.datetime.fromtimestamp(float(form.cleaned_data['end'])/1000.0) - timedelta(days=1)
        nut.start_time = s
        nut.expire_time = e
        nut.save()
    return HttpResponse()

@transaction.atomic
@login_required
def delete_plan(request, id):
    context = {}
    context['username'] = request.user.username
    try:
        nut = Nut.objects.get(id=id)
    except ObjectDoesNotExist:
        raise Http404("Nut does not exist")
    nut.delete()
    return redirect('/nuts/')


def post_key(nut):
    return nut.timestamp

# bw: search plan
@login_required
def search_plan(request):
    errors = []
    context = {'username': request.user.username}

    retrieved_nuts = {}
    res_nuts = []
    # flag == 0 represent there are at least one nuts to be retrieved
    context["flag"] = 0   
    if request.method == "GET":
        context["flag"] = 1
        context["errors"] = errors
        return render(request, "nuts/search.html", context)
    # check validation
    form = KeywordForm(request.POST)
    if not form.is_valid():
        context["flag"] = 1
        errors.append("Please enter the search keyword.")
    else:
        keyword = request.POST["keyword"].lower()
        # retrieve all the not expired nuts and sort them by the number of matching times
        now = datetime.datetime.now()
        nuts = sorted(Nut.objects.filter(privilege = 'Public').exclude(state='DONE').filter(expire_time__gte=now), key=post_key, reverse=True)

        for nut in nuts:
            matching = 0
            # count matching from nut's title and description
            title_words = re.split(';|,|\*|\?|\!|\.| *|\n', nut.title)
            for word in title_words:
                if word.lower() == keyword:
                    matching += 1
            des_words = re.split(';|,|\*|\?|\!|\.| *|\n', nut.description)
            for word in des_words:
                if word.lower() == keyword:
                    matching += 1
            # store in retrieve if matching not equal to 0 as a list, and dic will sort automatically
            if matching != 0:
                if retrieved_nuts.get(matching) == None:
                    retrieved_nuts[matching] = []
                retrieved_nuts[matching].append(nut)

        if len(retrieved_nuts) == 0:
            context["flag"] = 1
        else:
            # sort by descending order
            retrieved_nuts = OrderedDict(reversed(list(retrieved_nuts.items())))
            for key in retrieved_nuts.keys():

                lists = retrieved_nuts[key]
                for nut in lists:
                    res_nuts.append(nut)

    # add comments
    # append all the comment for each nut
    nut_id_set = set()
    for nut in res_nuts:
        nut_id_set.add(nut.id)
    allcomments = Comment.objects.all().order_by("timestamp")
    comments = []
    for comment in allcomments:
        if comment.nut.id in nut_id_set:
            comments.append(comment)
    context["comments"] = comments

    context["username"] = request.user.username
    
    # bw: like plans, get all the user's liked plan id
    squirrel = get_object_or_404(Squirrel, user = request.user)
    like_nuts = squirrel.like_plan

    like_nut_ids = []
    for like_nut in like_nuts.all():
        like_nut_ids.append(like_nut.id)
    context["like_nut_ids"] = like_nut_ids

    
    context['nuts'] = res_nuts
    return render(request, 'nuts/search.html', context)



