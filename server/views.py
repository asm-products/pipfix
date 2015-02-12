from rest_framework_mongoengine.viewsets import ModelViewSet
from server.documents import Vote, User, Stuff
from server.serializers import VoteSerializer, UserSerializer, StuffSerializer
from rest_framework_extensions.mixins import NestedViewSetMixin


class VoteViewSet(NestedViewSetMixin, ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    lookup_field = "stuff"

class UserViewSet(NestedViewSetMixin, ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
  
class StuffViewSet(NestedViewSetMixin, ModelViewSet):
    queryset = Stuff.objects.all()
    serializer_class = StuffSerializer
    lookup_field = "stuff_id"