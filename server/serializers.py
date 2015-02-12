from server.documents import Vote, User, Stuff
from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework.fields import EmailField

class VoteSerializer(DocumentSerializer):
    class Meta:
        model = Vote
        depth = 1
        fields = ('stuff', 'pips', 'user', 'comment')

class UserSerializer(DocumentSerializer):
    class Meta:
        model = User
        read_only_fields = ('id')
        extra_kwargs = {'followed': {'write_only': True}}
        fields = ('id', 'username', 'email', 'twitter_id', "followed")

class StuffSerializer(DocumentSerializer):
    class Meta:
        model = Stuff