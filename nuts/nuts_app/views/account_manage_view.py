from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import Http404

# for manually login a user
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth import login, authenticate
from nuts_app.models import *
from nuts_app.forms import * 
# used to send mail from within django
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator


def display_welcome(request):
    if request.user.is_authenticated():
        return redirect('/nuts/')
    return render(request, 'nuts/welcome.html', {})

# bw
def register(request):
    if request.user.is_authenticated():
        return redirect(reverse('home'))

    context = {}
    # display the registration form if this is a GET request
    if request.method == "GET":
        context["form"] = RegistrationForm()
        return render(request, "nuts/register.html", context)

    # otherwise get the form from POST request
    form = RegistrationForm(request.POST)
    context["form"] = form

    # check form validation
    if not form.is_valid():
        return render(request, "nuts/register.html", context)

    # call cleaned_data() defined in RegistrationForm to check errors
    new_user = User.objects.create_user(username=form.cleaned_data["username"],
                                        first_name=form.cleaned_data["firstname"],
                                        last_name=form.cleaned_data["lastname"],
                                        email=form.cleaned_data["email"],
                                        password=form.cleaned_data["password1"])

    # make user active after confirming the email address
    new_user.is_active = False

    new_user.save()

    # generate a one time token
    token = default_token_generator.make_token(new_user)

    email_body = """
Welcome to Nuts! Please click the link bellow to verify your email address
and complete the registration of your account:

    http://%s%s
""" % (request.get_host(), 
        reverse("confirm", args=(new_user.username, token)))

    send_mail(subject="Verify your email address",
              message=email_body,
              from_email="boweiz@andrew.cmu.edu",
              recipient_list=[new_user.email])

    context["email"] = form.cleaned_data["email"]

    # create profile and use a default image
    default_image = "default_image.jpg"
    new_profile = Squirrel(user=new_user, image=default_image)
    new_profile.save()

    return render(request, "account/needs-confirmation.html", context)

# bw
@transaction.atomic
def confirm_registration(request, username, token):

    user = get_object_or_404(User, username=username)

    # check the token
    if not default_token_generator.check_token(user, token):
        raise Http404
        
    # activate the user
    user.is_active = True
    user.save()
    return render(request, "account/confirmed.html", {})







