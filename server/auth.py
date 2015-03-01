from rest_framework.authentication import TokenAuthentication
from server.documents import User

class MyTokenAuthentication(TokenAuthentication):
    model = User

    