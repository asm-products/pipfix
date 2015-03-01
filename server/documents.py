from mongoengine import *
from mongoengine.django import auth
import binascii
import os

class Vote(Document):
    stuff = ReferenceField('Stuff')
    pips = IntField(min_value=1, max_value=10)
    user = ReferenceField('User', unique_with='stuff')
    comment = StringField(max_length=256)

    @property
    def username(self):
        return self.user.username

class User(auth.User):
    email = EmailField(required=False)
    twitter_id = IntField()
    followed = ListField(IntField())
    token = StringField(max_length=40, unique=True)

    def save(self, *args, **kwargs):
        if not self.id or not self.token:
            self.token = binascii.hexlify(os.urandom(20)).decode()

        super(User, self).save(*args, **kwargs)

class Stuff(Document):
    stuff_id = StringField(max_length=120, required=True, unique=True, primary_key=True)
    title = StringField(max_length=120, required=True)
    year = IntField()
    image = URLField()
    description = StringField()

    @property
    def average(self):
        return Vote.objects(stuff=self).average('pips')

class UserStuff(Document):
    user = ReferenceField('User', unique_with="stuff")
    stuff = ReferenceField('Stuff')

    @property
    def average(self):
        users = User.objects(twitter_id__in=self.user.followed)
        return Vote.objects(stuff=self.stuff, user__in=users).average('pips')

    @property
    def votes(self):
        users = User.objects(twitter_id__in=self.user.followed)
        return Vote.objects(stuff=self.stuff, user__in=users)

    @property
    def global_average(self):
        return self.stuff.average