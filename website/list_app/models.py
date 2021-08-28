from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.template.defaultfilters import slugify


GENDER = ((1, 'Male'), (0, 'Female'))
AGE = ((0, 'Adult'), (1, 'Child'), (2, 'Teenager'))


class Films(models.Model):
    genre = models.IntegerField(blank=True, null=True)
    hkmdb_id = models.IntegerField(blank=True, null=True)
    name_en = models.TextField(blank=True, null=True)
    name_zh = models.TextField(blank=True, null=True)
    visible = models.TextField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'films'

    def __str__(self):
        return str(self.genre)


class Sentences(models.Model):
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
    slug_c = models.SlugField(allow_unicode=True, unique=False, null=True, blank=True)

    class Meta:
        db_table = 'sentences'

    def save(self, *args, **kwargs):
        self.slug_c = slugify(self.orth)
        return super().save(*args, **kwargs)

    def calc_time(self, param):
        seconds = (param / 1000) % 60
        seconds = int(seconds)
        minutes = (param / (1000 * 60)) % 60
        minutes = int(minutes)
        hours = int((param / (1000 * 60 * 60)) % 24)
        time = "%d:%d:%d" % (hours, minutes, seconds)
        return time

    def converter_time_start(self):
        time_list = []
        calc_times = self.calc_time(self.timestamp_starts_at_ms)

        s = calc_times.split(':')
        for n in s:
            if len(n) == 1:
                time = str(0) + n
            else:
                time = n
            time_list.append(time)

        real_time = ":".join(time_list)
        return real_time

    def converter_time_end(self):
        time_list = []
        calc_times = self.calc_time(self.timestamp_ends_at_ms)

        s = calc_times.split(':')
        for n in s:
            if len(n) == 1:
                time = str(0) + n
            else:
                time = n
            time_list.append(time)

        real_time = ":".join(time_list)
        return real_time

    def real_time_duration(self):
        return self.timestamp_duration_ms

    def annot_func(self):
        orth_list = []
        tag_list = []
        pron_list = []
        multiple_list = []

        splitter = self.annotation_auto[1:].split("/")

        for x in splitter:
            multiple_list.append(x.split("_"))
        for obj in multiple_list:
            orth_list.append(obj[0])
            pron_list.append(obj[1])
            tag_list.append(obj[2])
        return {'context': zip(orth_list, pron_list, tag_list)}

    def get_absolute_url(self):
        fake_id = 0
        for orth in self.annot_func()['orth']:
            fake_id = id(orth)
        return reverse("search:details", fake_id)

    def annot_str(self):
        orth_list = []
        tag_list = []
        pron_list = []
        multiple_list = []

        splitter = self.annotation_string[1:].split("/")

        for x in splitter:
            multiple_list.append(x.split("_"))

        for obj in multiple_list:
            orth_list.append(obj[0])
            pron_list.append(obj[1])
            tag_list.append(obj[2])
        return {'context': zip(orth_list, pron_list, tag_list)}


class Tokens(models.Model):
    word_id = models.IntegerField(blank=True, null=True)
    sentence_id = models.IntegerField(blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'tokens'


class Words(models.Model):
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
        db_table = 'words'

    def __str__(self):
        return str(self.id)

    @classmethod
    def sum_freq(cls):
        return cls.objects.exclude(tag='Pu').aggregate(
            summation=Sum('freq')
        )['summation'] or 0


    @classmethod
    def rank(cls):
        words = cls.objects.all().exclude(tag='Pu')
        rank = 1
        rank_list = []
        while rank < words.count():
            rank_list.append(rank)
            rank += 1
        return rank_list


class Characters(models.Model):
    freq = models.IntegerField(blank=True, null=True)
    character = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'characters'


class Actors(models.Model):
    age = models.IntegerField(blank=True, null=True, choices=AGE)
    code = models.TextField(blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True, choices=GENDER)
    name_en = models.TextField(blank=True, null=True)
    name_zh = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'actors'

    def __str__(self):
        return str(self.age)