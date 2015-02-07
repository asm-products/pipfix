from server.documents import Vote, User
from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework.fields import EmailField

class VoteSerializer(DocumentSerializer):
  class Meta:
    model = Vote

class UserSerializer(DocumentSerializer):
  class Meta:
    model = User
    fields = ('username', 'email', 'twitter_id', "followed")