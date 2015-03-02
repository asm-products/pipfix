from rest_framework.authentication import TokenAuthentication
from server.documents import User
from rest_framework import exceptions
from django.utils.translation import ugettext_lazy as _

class MyTokenAuthentication(TokenAuthentication):
    model = User

    def authenticate_credentials(self, key):
        try:
            user = self.model.objects.get(token=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return (user, key)
