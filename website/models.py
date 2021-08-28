# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Actors(models.Model):
    id = models.IntegerField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    name_en = models.TextField(blank=True, null=True)
    name_zh = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'actors'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Characters(models.Model):
    id = models.IntegerField(blank=True, null=True)
    freq = models.IntegerField(blank=True, null=True)
    character = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'characters'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Films(models.Model):
    id = models.IntegerField(blank=True, null=True)
    genre = models.IntegerField(blank=True, null=True)
    hkmdb_id = models.IntegerField(blank=True, null=True)
    name_en = models.TextField(blank=True, null=True)
    name_zh = models.TextField(blank=True, null=True)
    visible = models.TextField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'films'


class Sentences(models.Model):
    id = models.IntegerField(blank=True, null=True)
    actor_id = models.IntegerField(blank=True, null=True)
    film_id = models.IntegerField(blank=True, null=True)
    media_code = models.IntegerField(blank=True, null=True)
    media_part = models.TextField(blank=True, null=True)
    timestamp_duration_ms = models.IntegerField(blank=True, null=True)
    timestamp_ends_at_ms = models.IntegerField(blank=True, null=True)
    timestamp_starts_at_ms = models.IntegerField(blank=True, null=True)
    transcription = models.TextField(blank=True, null=True)
    annotation_auto = models.TextField(blank=True, null=True)
    annotation_string = models.TextField(blank=True, null=True)
    alpha = models.TextField(blank=True, null=True)
    characters_string = models.TextField(blank=True, null=True)
    num_characters = models.IntegerField(blank=True, null=True)
    num_tokens = models.IntegerField(blank=True, null=True)
    orth = models.TextField(blank=True, null=True)
    pron = models.TextField(blank=True, null=True)
    tag = models.TextField(blank=True, null=True)
    tokens_string = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sentences'


class Tokens(models.Model):
    id = models.IntegerField(blank=True, null=True)
    word_id = models.IntegerField(blank=True, null=True)
    sentence_id = models.IntegerField(blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tokens'


class Words(models.Model):
    id = models.IntegerField(blank=True, null=True)
    orth = models.TextField(blank=True, null=True)
    tag = models.TextField(blank=True, null=True)
    pron = models.TextField(blank=True, null=True)
    alpha = models.TextField(blank=True, null=True)
    freq = models.IntegerField(blank=True, null=True)
    freq_adult = models.IntegerField(blank=True, null=True)
    freq_child = models.IntegerField(blank=True, null=True)
    freq_teenager = models.IntegerField(blank=True, null=True)
    freq_female = models.IntegerField(blank=True, null=True)
    freq_male = models.IntegerField(blank=True, null=True)
    freq_comedy = models.IntegerField(blank=True, null=True)
    freq_crime = models.IntegerField(blank=True, null=True)
    freq_drama = models.IntegerField(blank=True, null=True)
    freq_1943 = models.IntegerField(blank=True, null=True)
    freq_1947 = models.IntegerField(blank=True, null=True)
    freq_1948 = models.IntegerField(blank=True, null=True)
    freq_1950 = models.IntegerField(blank=True, null=True)
    freq_1951 = models.IntegerField(blank=True, null=True)
    freq_1952 = models.IntegerField(blank=True, null=True)
    freq_1953 = models.IntegerField(blank=True, null=True)
    freq_1954 = models.IntegerField(blank=True, null=True)
    freq_1955 = models.IntegerField(blank=True, null=True)
    freq_1956 = models.IntegerField(blank=True, null=True)
    freq_1957 = models.IntegerField(blank=True, null=True)
    freq_1958 = models.IntegerField(blank=True, null=True)
    freq_1959 = models.IntegerField(blank=True, null=True)
    freq_1960 = models.IntegerField(blank=True, null=True)
    freq_1961 = models.IntegerField(blank=True, null=True)
    freq_1962 = models.IntegerField(blank=True, null=True)
    freq_1963 = models.IntegerField(blank=True, null=True)
    freq_1964 = models.IntegerField(blank=True, null=True)
    freq_1965 = models.IntegerField(blank=True, null=True)
    freq_1966 = models.IntegerField(blank=True, null=True)
    freq_1967 = models.IntegerField(blank=True, null=True)
    freq_1968 = models.IntegerField(blank=True, null=True)
    freq_1969 = models.IntegerField(blank=True, null=True)
    freq_1970 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'words'
