from server.documents import Vote, User
from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework.fields import EmailField

class VoteSerializer(DocumentSerializer):
    class Meta:
        model = Vote
        fields = ('stuff_id', 'pips', 'user', 'comment')

class UserSerializer(DocumentSerializer):
    class Meta:
        model = User
        read_only_fields = ('id')
        fields = ('id', 'username', 'email', 'twitter_id', "followed")