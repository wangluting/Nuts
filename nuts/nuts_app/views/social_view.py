from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from nuts_app.models import *
from django.http import HttpResponse

def eat_plan(request, do_follow, id):
    context = {'username': request.user.username}
    squirrel = get_object_or_404(Squirrel, user = request.user)
    try:
        nut = Nut.objects.get(id=id)
    except ObjectDoesNotExist:
        raise Http404("Nut does not exist")
    if do_follow == 'True':
        squirrel.follow_plan.add(nut)
    else:
        squirrel.follow_plan.remove(nut)
    
    #return HttpResponse()
    return render(request, 'nuts/view_single_plan.html', context)


# bw: like plan
def like_plan(request, do_like, id):
    context = {'username': request.user.username}
    
    squirrel = get_object_or_404(Squirrel, user = request.user)
    try:
        nut = Nut.objects.get(id=id)
    except ObjectDoesNotExist:
        raise Http404("Nut does not exist")

    if do_like == 'True':
        # add into user
        squirrel.like_plan.add(nut)
        # add into nut as well
        nut.liked_user.add(squirrel)
    else:
        squirrel.like_plan.remove(nut)
        nut.liked_user.remove(squirrel)
    
    return HttpResponse()


def follow_user(request, do_follow, id):
    context = {'username': request.user.username}
    squirrel = get_object_or_404(Squirrel, user = request.user)
    try:
        user = User.objects.get(id=id)
    except ObjectDoesNotExist:
        raise Http404("User does not exist")
    try:
        squirrel_fol = Squirrel.objects.get(user=user)
    except ObjectDoesNotExist:
        raise Http404("Nut does not exist")
    if do_follow == 'True':
        squirrel.follow_user.add(squirrel_fol)
    else:
        squirrel.follow_user.remove(squirrel_fol)
    
    return HttpResponse()