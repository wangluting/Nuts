"# -- coding: utf-8 --"

from __future__ import unicode_literals
from django.utils.html import escape
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import default
from channels import Group
import json

# Create your models here.

# lutingw: Nuts: plan
class Nut(models.Model):
    PRIVILEGE_CHOICES = (('Public', 'Public',), ('Private', 'Private',))
    STATE_CHOICES = (('TODO', 'todo'), ('DOING', 'doing'), ('DONE', 'done'))

    author = models.ForeignKey(User)  # the user who created the plan
    timestamp = models.DateTimeField(default=timezone.now)  # time the plan is created
    title = models.CharField(max_length=100)  # title of the plan, a brief description
    description = models.TextField(max_length=5000)  # detailed description of the plan
    privilege = models.CharField(max_length=7, choices=PRIVILEGE_CHOICES)  # public or private
    start_time = models.DateField(default=timezone.now)  # time that this plan would start
    expire_time = models.DateField(default=timezone.now)  # time that this plan would expire
    state = models.CharField(max_length=5, choices=STATE_CHOICES, default='TODO') # state
    lat = models.FloatField(default=0, max_length=100)
    lng = models.FloatField(default=0, max_length=100)
    # bw: like nut
    liked_user = models.ManyToManyField('Squirrel', blank=True)      # the list of user that like this nut
    # liu3:
    point = models.DecimalField(decimal_places=0, max_digits=5, default=0); 

    # display each nut
    def __unicode__(self):
        return '%s %s %s %s %s %s %s %f %f %s' % (self.author, self.timestamp, self.expire_time, self.title, self.description, self.privilege, self.state, self.lat, self.lng, self.reference)

    # get all TUDO nuts
    @staticmethod
    def get_todo(user):
        return Nut.objects.filter(author=user, state='TODO').order_by('-expire_time')[:10]

    # get all DOING nuts
    @staticmethod
    def get_doing(user):
        return Nut.objects.filter(author=user, state='DOING').order_by('-expire_time')[:10]

    # get all DOING nuts
    @staticmethod
    def get_done(user):
        return Nut.objects.filter(author=user, state='DONE').order_by('-expire_time')[:10]

    # get all nuts
    @staticmethod
    def get_all(user):
        return Nut.objects.filter(author=user).order_by('-expire_time')

    @property
    def html(self):
        return "<div>" \
               "<div class='row wide' id='nut_%d'>" \
               "<div class='col-md-4 left'><p id='nutExpiretime'>%s</p></div>" \
               "<div class='col-md-6 left'>" \
               "<a href='/nuts/view-plan/%d' id='nutTitle_nut_%d'>%s</a></div>" \
               "<div class='col-md-2 right'><p id='nutPrivilege'>%s</p></div>" \
               "</div></div>" % (self.id, self.expire_time, self.id, self.id, escape(self.title), self.privilege)
               # bw add  id='nutTitle_nut_%d' for "surprise" showing in home page

               
# bw: Squirrel : user's profile
class Squirrel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)     # the user
    # follow_plan = models.ManyToManyField(Nut)       # the list of plans that the user follows
    # follow_user = models.ManyToManyField(User)      # the list of users that the user follows

    # bw: max_digits=5,  triger error
    age = models.DecimalField(decimal_places=0, max_digits=5, blank=True, null=True);  # age of the user
    image = models.ImageField(upload_to="addr-icon-photos", null=True)      # the image of the user
    location = models.CharField(max_length=100, blank=True)         # location of the user
    description = models.CharField(max_length=300, blank=True)      # short description about the user
    # liu3
    follow_plan = models.ManyToManyField(Nut, blank=True, related_name='follow_plan')       # the list of plans that the user follows
    follow_user = models.ManyToManyField("self", symmetrical=False, blank=True)      # the list of users that the user follows
    point = models.DecimalField(decimal_places=0, max_digits=5, default=0);     # points

    # bw: like nut
    like_plan = models.ManyToManyField(Nut, blank=True, related_name='like_plan')      # the list of nuts that this user like


# bw: comment
class Comment(models.Model):
    nut = models.ForeignKey(Nut, on_delete=models.CASCADE)
    text = models.CharField(max_length=42)
    timestamp = models.DateTimeField(default=timezone.now)  # time the comment is created
    user = models.ForeignKey(User, on_delete=models.CASCADE)

#liu3: room for each one to one chat
class Room(models.Model):
    # Room title
    title = models.CharField(max_length=255)
    room_id = models.CharField(max_length=255)

    @property
    def websocket_group(self):
        return Group("room-%s" % self.room_id)

    def send_message(self, message, user):
        msg = Message(room_id=self.room_id, message=message, sender_id=user.id, sender_username=user.username)
        msg.save()

        final_msg = {'room': str(self.id), 'message': message, 'username': user.username, 'id': user.id}

        # Send out the message to everyone in the room
        self.websocket_group.send(
            {"text": json.dumps(final_msg)}
        )
# liu3: store the message
class Message(models.Model):
    room_id = models.CharField(max_length=255)
    message = models.CharField(max_length=2000)
    timestamp = models.DateTimeField(default=timezone.now)
    sender_id = models.CharField(max_length=255, default='')
    sender_username = models.CharField(max_length=255, default='')

