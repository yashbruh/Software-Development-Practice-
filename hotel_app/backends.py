from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to get the user by email (username is passed as email in this case)
            user = CustomUser.objects.get(email=username)
            if user.check_password(password):  # Check if the password is correct
                return user
        except CustomUser.DoesNotExist:
            return None  # User not found
