from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):

    def create_user(self, id, password, **extra_fields):
        user = self.model(id=id, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    