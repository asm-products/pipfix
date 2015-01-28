from rest_framework_mongoengine.viewsets import ModelViewSet
from server.documents import Vote
from server.serializers import VoteSerializer


class VoteViewSet(ModelViewSet):
  queryset = Vote.objects.all()
  serializer_class = VoteSerializer
  lookup_field = "stuff_id"
