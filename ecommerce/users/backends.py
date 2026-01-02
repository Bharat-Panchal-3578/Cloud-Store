from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, useranme=None, email=None, password=None, **kwargs):
        if password is None:
            return None

        try:
            if email:
                user = User.objects.get(email=email)
            elif useranme:
                user = User.objects.get(username=useranme)
            else:
                return None
            
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None
