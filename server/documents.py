from mongoengine import *
from mongoengine.django import auth

class Vote(Document):
  stuff_id = StringField(max_length=120, required=True, unique=True)
  pips = IntField(min_value=1, max_value=10)

class User(auth.User):
  email = EmailField(required=False)
  twitter_id = IntField()
  followed = ListField(IntField())
