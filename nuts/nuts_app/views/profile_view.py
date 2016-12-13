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

from mimetypes import guess_type
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# show others profile
@login_required
def show_profile(request, user_id):

    errors = []
    context = {}
    flag = 2
    # check initial flag
    if "flag" in request.POST and request["flag"]:
        flag = 1
    try:
        user = User.objects.get(id=user_id)
        profile = get_object_or_404(Squirrel, user=user)
        nuts = Nut.objects.filter(author=user).order_by("-timestamp")
        context = {"user":user, "profile":profile, 'nuts': nuts}

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

        # check self
        if (request.user == user):
            flag = 1
        else:
            sq_cur = Squirrel.objects.get(user=request.user)
            if profile in sq_cur.follow_user.all():
                context['follow'] = False
            else:
                context['follow'] = True

        # bw: like plans, get all the user's liked plan id
        squirrel = get_object_or_404(Squirrel, user = request.user)
        like_nuts = squirrel.like_plan

        like_nut_ids = []
        for like_nut in like_nuts.all():
            like_nut_ids.append(like_nut.id)
        context["like_nut_ids"] = like_nut_ids

    except ObjectDoesNotExist:
        errors.append("This user does not exist.")
        context["errors"] = errors

    context["username"] = request.user.username
    context["flag"] = flag
    return render(request, "nuts/profile.html", context)

@login_required
@transaction.atomic
def edit_profile(request):

    context = {}
    profile_to_edit = get_object_or_404(Squirrel, user=request.user)

    nuts = Nut.objects.filter(author=request.user)
    context["nuts"] = nuts
    context["username"] = request.user.username
    context["user"] = request.user
    context["profile"] = profile_to_edit

    # when hit the edit button on selfprofile page
    if request.method == "GET":
        form = ProfileForm(instance=profile_to_edit)  # Creates form from the
        context["form"] = form             # existing profile
        return render(request, "nuts/edit_profile.html", context)

    # otherwise get all the data to update the model if method is POST
    form = ProfileForm(request.POST, request.FILES, instance=profile_to_edit)

    # check validation
    if not form.is_valid():
        context["form"] = form
        return render(request, "nuts/edit_profile.html", context)

    form.save()

    context["form"] = form
    context["flag"] = 1
    return render(request, "nuts/profile.html", context)

@login_required
def get_photo(request, user_id):
    cur_user = User.objects.filter(id=user_id)
    profile = get_object_or_404(Squirrel, user=cur_user)
    if not profile.image:
        raise Http404

    content_type = guess_type(profile.image.name)
    return HttpResponse(profile.image, content_type=content_type)

# bw
@login_required
def get_default_photo(request):
    cur_user = User.objects.filter(id=request.user.id)
    profile = get_object_or_404(Squirrel, user=cur_user)
    if not profile.image:
        raise Http404

    content_type = guess_type(profile.image.name)
    return HttpResponse(profile.image, content_type=content_type)

@login_required
@transaction.atomic
def change_password(request):

    profile = get_object_or_404(Squirrel, user=request.user)
    form = ProfileForm(instance=profile) 
    nuts = Nut.objects.filter(author=request.user)
    
    context = {"user":request.user, "username":request.user.username, "form":form, "profile":profile, "nuts":nuts}
    changepassworderrors = []

    passwordform = PasswordChangeForm(user=request.user)
    if request.method == "POST":
        passwordform = PasswordChangeForm(user=request.user, data=request.POST)

        if passwordform.is_valid():
            context["messages"] = []
            context["messages"].append("Changed your password successfully.")
            passwordform.save()
            # for not logout the user
            update_session_auth_hash(request, passwordform.user)

    context["passwordform"] = passwordform
    context["flag"] = 1

    return render(request, "nuts/profile.html", context)
