from rest_framework_mongoengine.viewsets import ModelViewSet
from server.documents import Vote, User
from server.serializers import VoteSerializer, UserSerializer


class VoteViewSet(ModelViewSet):
  queryset = Vote.objects.all()
  serializer_class = VoteSerializer
  lookup_field = "stuff_id"

class UserViewSet(ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  
