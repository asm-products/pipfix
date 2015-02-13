from mongoengine import *
from mongoengine.django import auth


class Vote(Document):
    stuff = ReferenceField('Stuff')
    pips = IntField(min_value=1, max_value=10)
    user = ReferenceField('User')
    comment = StringField(max_length=256)

class User(auth.User):
    email = EmailField(required=False)
    twitter_id = IntField()
    followed = ListField(IntField())

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
