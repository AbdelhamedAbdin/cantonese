from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.template.defaultfilters import slugify
import re


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True, blank=False)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    date_joined = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    user_signed = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.email

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    def has_perm(self, perm, obj=None):
        return True

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])


post_save.connect(receiver=create_profile, sender=User)


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_history')
    history = models.CharField(max_length=255, blank=True)
    verb_option = models.CharField(max_length=30, default="POS", blank=False)
    action_option = models.CharField(max_length=15, default="contains", blank=False)
    history_time = models.DateField(auto_now_add=True)
    deleted_history = models.BooleanField(default=False)
    advanced_search = models.BooleanField(default=False)

    class Meta:
        ordering = ('-history_time',)

    def __str__(self):
        return str(self.id)

    def compileFunction(cls, pattern, string):
        re_obj = re.compile(pattern)
        return re_obj.findall(string)

    def text_spliter(self):
        query_obj = self.compileFunction("[\u4e00-\u9fff]+|[？]|[。]|[，]|[…]|[！]|[a-zA-Z0-9]+", self.history)
        return query_obj

    def verb_spliter(self):
        verb_obj = self.compileFunction("[a-zA-Z ]+", self.verb_option)
        return verb_obj

    def action_spliter(self):
        action_obj = self.compileFunction("[a-zA-Z _]+", self.action_option)
        return action_obj
