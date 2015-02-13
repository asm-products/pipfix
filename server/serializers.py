from server.documents import Vote, User, Stuff, UserStuff
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
        fields = ('stuff_id', 'title', 'year', 'image', 'description', 
            'average')
        read_only_fields = ('average',)

class UserStuffSerializer(DocumentSerializer):
    user = UserSerializer()
    stuff = StuffSerializer()

    class Meta:
        model = UserStuff
        fields = ('stuff', 'user', 'average')
        read_only_fields = 'average'