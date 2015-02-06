from server.documents import Vote
from rest_framework_mongoengine.serializers import DocumentSerializer

class VoteSerializer(DocumentSerializer):
  class Meta:
    model = Vote
