from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.models import User
from models import *
import datetime

# bw: for register
class RegistrationForm(forms.Form):
    firstname = forms.CharField(max_length=40, label="First name")
    lastname = forms.CharField(max_length=40, label="Last name")
    username = forms.CharField(max_length=40, label="User name")

    email = forms.EmailField(max_length=80, 
                            label="Email address",
                            widget=forms.EmailInput())
    password1 = forms.CharField(max_length=200,
                                label="Passwowrd",
                                widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=200,
                                label="Confirm passwowrd",
                                widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        email = cleaned_data.get("email")
        if User.objects.filter(email=email):
            raise forms.ValidationError("This email address is already taken.")

        username = cleaned_data.get("username")
        if User.objects.filter(username=username):
            raise forms.ValidationError("This username is already taken.")


        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwowrds did not match.")
        elif len(password1) < 8:
            raise forms.ValidationError("This password is too short. It must contain at least 8 characters.")
        # check pure numeric
        else:
            try:
                int(password1)
                raise forms.ValidationError("This password is entirely numeric.")
            except ValueError:
                pass
                
        return cleaned_data

# bw
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Squirrel
        exclude = {"user", "follow_plan", "follow_user", "like_plan", "point"}
        widgets = {"picture" : forms.FileInput()}


# lutingw edit plan form
# title can not be changed, and state can be changed.
class EditPlanForm(forms.ModelForm):
    class Meta:
        model = Nut
        widgets = {'title': forms.Textarea(attrs={'readonly':'readonly', 'rows': 1, 'cols': '80%'}),
                   'description': forms.Textarea(attrs={'placeholder': 'Detailed description', 'rows': 4, 'cols': '80%'}),
                   'start_time': SelectDateWidget(),
                   'expire_time': SelectDateWidget(),
                   'privilege': forms.Select(),
                   'state': forms.Select()}
        exclude = ('author', 'timestamp', 'lat', 'lng', 'liked_user', 'point')

    def clean_expire_time(self):
        expire_time = self.cleaned_data.get('expire_time')
        if expire_time < datetime.date.today():
            raise forms.ValidationError("Expire time must no less than today.")

        return expire_time

# lutingw create plan form
# state can not be set, the default is todo
class PlanForm(forms.ModelForm):
    expire_same = forms.BooleanField(label="Expire date same as start date", initial=True, required=False)
    class Meta:
        model = Nut
        widgets = {'title': forms.Textarea(attrs={'placeholder': 'Title', 'rows': 1, 'cols': '80%'}),
                   'description': forms.Textarea(attrs={'placeholder': 'Detailed description', 'rows': 4, 'cols': '80%'}),
                   'start_time': SelectDateWidget(),
                   'expire_time': SelectDateWidget(),
                   'privilege': forms.Select()}

        exclude = ('author','timestamp','state', 'lat', 'lng', 'liked_user', 'point')

    # check whether expired time is before today
    def clean_expire_time(self):
        expire_time = self.cleaned_data.get('expire_time')
        if expire_time < datetime.date.today():
            raise forms.ValidationError("Expire time must no less than today.")

        return expire_time


# liu3 use form to validate modify plan time using Ajax
class PlanTimeForm(forms.Form):
    id = forms.CharField(max_length=40)
    start = forms.IntegerField()
    end = forms.IntegerField()

class TimeRangeForm(forms.Form):
    start = forms.IntegerField()
    end = forms.IntegerField()

class RoomIdForm(forms.Form):
    room_id = forms.CharField(max_length=255)

# bw use for validate search keywords
class KeywordForm(forms.Form):
    keyword = forms.CharField(max_length=40)

class CommentForm(forms.Form):
    comment = forms.CharField(max_length=42)
    nut_id = forms.CharField(max_length=40)


