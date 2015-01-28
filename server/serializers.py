from server.documents import Vote
from rest_framework_mongoengine.serializers import MongoEngineModelSerializer

class VoteSerializer(MongoEngineModelSerializer):
  class Meta:
    model = Vote
