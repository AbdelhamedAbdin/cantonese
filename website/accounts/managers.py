from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, password, **extra_data):
        if not email:
            raise ValueError('email must be set')

        if username is None:
            raise TypeError('Users must have a username.')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username.lower(),
            password=password,
            **extra_data
        )
        user.username = username.lower()
        user.set_password(user.password)
        # user.is_superuser = True
        # user.admin = True
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_data):
        extra_data.setdefault('is_superuser', False)
        extra_data.setdefault('admin', False)
        extra_data.setdefault('staff', True)
        return self._create_user(email, username, password, **extra_data)

    def create_superuser(self, email, username, password, **extra_data):
        extra_data.setdefault('is_superuser', True)
        extra_data.setdefault('admin', True)
        extra_data.setdefault('staff', True)
        extra_data.setdefault('user_signed', True)
        return self._create_user(email, username, password, **extra_data)
