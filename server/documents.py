from mongoengine import *

class Vote(Document):
  stuff_id = StringField(max_length=120, required=True, unique=True)
  pips = IntField(min_value=1, max_value=10)