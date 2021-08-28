from django.shortcuts import render, redirect
from list_app.models import Words, Sentences, Films, Actors, Tokens
from django.db.models import Q
from django.core.paginator import Paginator
from accounts.models import User, History
from django.http import HttpResponseRedirect
import pandas as pd
import re
import sqlite3
from website.settings import BASE_DIR


# group for all objects
def filters(request):
    context = {
        'actors': Actors.objects.all(),
        'films': Films.objects.all(),
        'words': Words.objects.all()
    }
    return context


# Search, Filter
def search(request):
    filtering = filters(request)
    sentence = Sentences.objects.all()
    words = Words.objects.all()
    next_url = ''
    prev_url = ''
    actors_id = []
    actors_gender = []
    actors_age = []

    films_id = []
    films_genre = []
    films_from = []
    films_to = []

    actor = request.GET.get('actor')
    gender = request.GET.get('gender')
    age = request.GET.get('age')

    film = request.GET.get('film')
    genre = request.GET.get('genre')
    fromm = request.GET.get('from')
    too = request.GET.get('to')
    multipleSearch = None

    actorr = None
    if actor and actor != 'all':
        actorr = Actors.objects.get(id=int(actor))

    genderr = None
    if gender and gender != 'all':
        genderr = gender

    agee = None
    if age and age != 'all':
        agee = age

    filmm = None
    if film and film != 'all':
        filmm = Films.objects.get(id=int(film))

    genree = None
    if genre and genre != 'all':
        genree = genre

    frommm = None
    if fromm and fromm != 'all':
        frommm = int(fromm)

    tooo = None
    if too and too != 'all':
        tooo = int(too)

    if "actor" in request.GET:
        if actor == 'all':
            actors = Actors.objects.all()
            sentence = sentence
        else:
            actors = Actors.objects.filter(id=int(actor))
            for act in actors:
                actors_id.append(Actors.objects.get(id=int(act.id)).id)
            sentence = sentence.filter(actor_id__in=actors_id)

        if gender == 'all':
            actors = actors
            sentence = sentence
        else:
            actors = actors.filter(gender=int(gender))
            for act in actors:
                actors_gender.append(Actors.objects.get(id=int(act.id)).id)
            sentence = sentence.filter(actor_id__in=actors_gender)

        if age == 'all':
            actors = actors
            sentence = sentence
        else:
            actors = actors.filter(age=int(age))
            for act in actors:
                actors_age.append(Actors.objects.get(id=int(act.id)).id)
            sentence = sentence.filter(actor_id__in=actors_age)

    if "film" in request.GET:
        if film == 'all':
            films = Films.objects.all()
            sentence = sentence
        else:
            films = Films.objects.filter(id=int(film))
            for film in films:
                films_id.append(Films.objects.get(id=int(film.id)).id)
            sentence = sentence.filter(film_id__in=films_id)

        if genre == 'all':
            films = films
            sentence = sentence
        else:
            films = films.filter(genre=int(genre))
            for film in films:
                films_genre.append(Films.objects.get(id=int(film.id)).id)
            sentence = sentence.filter(film_id__in=films_genre)

        if fromm == 'all':
            films = films
            sentence = sentence
        else:
            films = films.filter(year__gte=int(fromm))
            for film in films:
                films_from.append(Films.objects.get(id=int(film.id)).id)
            sentence = sentence.filter(film_id__in=films_from)

        if too == 'all':
            films = films
            sentence = sentence
        else:
            films = films.filter(year__lte=int(too))
            for film in films:
                films_to.append(Films.objects.get(id=int(film.id)).id)
            sentence = sentence.filter(film_id__in=films_to)
    import re
    if request.method == "GET":
        # the query name of search formsets
        # try:
        if "query" in request.GET:
            # One search field case
            if len(request.GET.getlist('query')) == 1:
                multipleSearch = None
                user = User.objects.get(username=request.user.username)
                request_query = request.GET.get('query', "")
                verb_option = request.GET.get("verb_option", "")

                if verb_option == "":
                    v = "POS"
                elif verb_option == "Adj":
                    v = "Adj"
                elif verb_option == "Adv":
                    v = "Adv"
                elif verb_option == "Asp":
                    v = "Asp"
                elif verb_option == "Cl":
                    v = "Cl"
                elif verb_option == "Conj":
                    v = "Conj"
                elif verb_option == "Det":
                    v = "Det"
                elif verb_option == "Idiom":
                    v = "Idiom"
                elif verb_option == "Intj":
                    v = "Intj"
                elif verb_option == "Noun":
                    v = "Noun"
                elif verb_option == "Num":
                    v = "Num"
                elif verb_option == "Ono":
                    v = "Ono"
                elif verb_option == "Part":
                    v = "Part"
                elif verb_option == "Prep":
                    v = "Prep"
                elif verb_option == "Pro":
                    v = "Pro"
                elif verb_option == "Pu":
                    v = "Pu"
                elif verb_option == "SFP":
                    v = "SFP"
                elif verb_option == "Verb":
                    v = "Verb"
                elif verb_option == "X":
                    v = "X"
                else:
                    v = verb_option
                History.objects.create(
                    user=user,
                    history=request_query,
                    verb_option=v,
                    action_option=request.GET.get('formsets_option', 'contains'),
                    advanced_search=False
                )

                if request_query == "":
                    if verb_option == "":
                        return redirect("search:search")
                    sentence = sentence.exclude(tag='Pu').filter(tag__contains=verb_option)
                    words = words.exclude(tag='Pu').filter(tag__contains=verb_option)
                else:
                    # loop sentence
                    if request.GET['formsets_option'] == "contains":
                        sentence = sentence.filter(
                            Q(pron__contains=request_query) |
                            Q(tag__contains=request_query) |
                            Q(orth__contains=request_query)
                            ).exclude(tag='Pu').filter(tag__contains=verb_option)

                        words = words.filter(
                            Q(pron__contains=request_query) |
                            Q(orth__contains=request_query)
                                   ).exclude(tag='Pu').filter(tag__contains=verb_option)

                    elif request.GET['formsets_option'] == "is":
                        sentence = sentence.filter(
                            Q(pron__iexact=request_query) |
                            Q(tag__iexact=request_query) |
                            Q(orth__iexact=request_query)
                            ).exclude(tag='Pu').filter(tag__contains=verb_option)

                        words = words.filter(
                            Q(pron__iexact=request_query) |
                            Q(orth__iexact=request_query)
                                             ).exclude(tag='Pu').filter(tag__contains=verb_option)

                    elif request.GET['formsets_option'] == "start_with":
                        sentence = sentence.filter(
                            Q(pron__startswith=request_query) |
                            Q(tag__startswith=request_query) |
                            Q(orth__startswith=request_query)
                            ).exclude(tag='Pu').filter(tag__contains=verb_option)

                        words = words.filter(
                            Q(pron__startswith=request_query) |
                            Q(orth__startswith=request_query)
                                            ).exclude(tag='Pu').filter(tag__contains=verb_option)

                    elif request.GET['formsets_option'] == "end_with":
                        sentence = sentence.filter(
                            Q(pron__endswith=request_query) |
                            Q(tag__endswith=request_query) |
                            Q(orth__endswith=request_query)
                            ).exclude(tag='Pu').filter(tag__contains=verb_option)

                        words = words.filter(
                            Q(pron__endswith=request_query) |
                            Q(orth__endswith=request_query)
                                             ).exclude(tag='Pu').filter(tag__contains=verb_option)
            # Multiple search field case
            else:
                conn = sqlite3.connect(BASE_DIR / 'db.sqlite3')
                tokens = pd.read_sql_query('SELECT * FROM tokens', conn)
                words = pd.read_sql_query('SELECT * FROM words', conn)
                sentences = pd.read_sql_query('SELECT * FROM sentences', conn)
                multipleSearch = "query"
                user = User.objects.get(username=request.user.username)
                request_query = request.GET.getlist('query')
                request_formsets = request.GET.getlist('formsets_option')
                verb_option = request.GET.getlist("verb_option")
                v_list = []

                for v_option in verb_option:
                    if v_option == "":
                        v = "POS"
                    else:
                        v = verb_option
                    v_list.append(v)

                History.objects.create(
                    user=user,
                    history=request_query,
                    verb_option=v_list,
                    action_option=request_formsets,
                    advanced_search=False
                )
                inc = 0
                query = []
                sentence_words_id = None
                # loop sentence
                w = ", ".join(request_query)
                duplicated_word_query = len(re.findall(request_query[0], w))

                for n, q in enumerate(request_query):
                    # there's query data coming from search
                    if q != "":
                        # independent words for word tap
                        if "contains" == request_formsets[inc]:
                            w = words[words['orth'].str.contains(q, na=False)][['id']]
                            w['query'] = n
                            query.append(w)
                        elif "is" == request_formsets[inc]:
                            w = words[words['orth'] == q][['id']]
                            w['query'] = n
                            query.append(w)
                        elif "start_with" == request_formsets[inc]:
                            w = words[words['orth'].str.contains(pat=f'^{q}', regex=True, na=False)][['id']]
                            w['query'] = n
                            query.append(w)
                        elif "end_with" == request_formsets[inc]:
                            w = words[words['orth'].str.contains(pat=f'{q}$', regex=True, na=False)][['id']]
                            w['query'] = n
                            query.append(w)
                    inc += 1

                pd.set_option('display.max_rows', None)
                pd.set_option('display.max_columns', None)
                query = pd.concat([q for q in query])
                query['query'] += 1
                # print(query)
                tokens = tokens[['word_id', 'sentence_id', 'position']]
                token_query = tokens.merge(query, left_on='word_id', right_on='id')
                token_query = token_query.sort_values(by=['sentence_id', 'position'])
                # print(token_query.head(200))
                if duplicated_word_query > 1:
                    token_query['next_position'] = token_query.groupby("sentence_id")['position'].shift(-3)
                    token_query['next_query'] = token_query.groupby("sentence_id")['query'].shift(-3)
                else:
                    token_query['next_position'] = token_query.groupby("sentence_id")['position'].shift(-1)
                    token_query['next_query'] = token_query.groupby("sentence_id")['query'].shift(-1)

                token_query['position_diff'] = token_query['next_position'] - token_query['position']
                token_query['query_diff'] = token_query['next_query'] - token_query['query']

                selected_sentence = token_query[(token_query['position_diff'] == 1) & (token_query['query_diff'] == 1)]
                if duplicated_word_query > 1:
                    sentence_id = selected_sentence[['sentence_id']].drop_duplicates()
                else:
                    sentence_id = selected_sentence[['sentence_id']]
                # print(sentence_id)
                sentence = sentences.merge(sentence_id, left_on='id', right_on='sentence_id')
                # print(sentence.count())
                sentence_query = sentence['sentence_id'].to_list()
                sentence = Sentences.objects.all().filter(id__in=sentence_query)

        elif "query" in request.GET and "formsets_option" not in request.GET:
            return redirect("search:search")
        # except:
        #     return redirect("search:search")

    if sentence:
        paginator = Paginator(sentence, 20)
        page_number = request.GET.get('page_number')
        sentence = paginator.get_page(page_number)
        if sentence.has_next():
            next_url = f"{request.get_raw_uri()}&page_number={sentence.next_page_number()}"
        else:
            next_url = ''

        if sentence.has_previous():
            prev_url = f"{request.get_raw_uri()}&page_number={sentence.previous_page_number()}"
        else:
            prev_url = ''

    if len(request.GET.getlist('query')) == 1:
        if words:
            paginator = Paginator(words, 50)
            page_number = request.GET.get('page_numberr')
            words = paginator.get_page(page_number)
    else:
        words = 0

    context = {
        'sentences': sentence,
        'words': words,
        'filter': filtering,
        'verb_option': request.GET.get("verb_option"),
        'formsets_option': request.GET.get("formsets_option"),
        'actorr': actorr,
        'genderr': genderr,
        'agee': agee,
        'filmm': filmm,
        'genree': genree,
        'frommm': frommm,
        'tooo': tooo,
        'next_url': next_url,
        'prev_url': prev_url,
        'from_to_year': Films.objects.all().order_by('year').values_list('year', flat=True).distinct(),
        'query_length': request.GET.getlist('query'),
        'multipleSearch': multipleSearch,
        'multiple_requests': zip(request.GET.getlist('query'), request.GET.getlist('formsets_option'), request.GET.getlist('verb_option'))
    }
    return render(request, "search/search.html", context)


# Search details section
def search_details(request, slug=None):
    word = None
    freq_female_list = []
    freq_by_year_x = []

    if slug:
        try:
            word = Words.objects.filter(orth=slug, tag=request.GET.get("verb_option", ""), pron=request.GET.get("jyutping", ""))
            for w in word:
                freq_female_list.append(w.freq_female)
        except:
            return redirect("accounts:index_404")

    try:
        max_female = max(freq_female_list)
    except:
        try:
            freq_female_list = []
            word = Words.objects.filter(orth=slug)
            for w in word:
                freq_female_list.append(w.freq_female)
            max_female = max(freq_female_list)
        except:
            return redirect('accounts:index_404')
    seeking = word.get(freq_female=max_female)
    # number of sentences by word
    word_id = seeking.id
    token = Tokens.objects.filter(word_id=word_id).distinct().values_list('sentence_id', flat=True).distinct()

    for years in range(1943, 1971):
        if years not in [1944, 1945, 1946, 1949]:
            freq_by_year_x.append(years)

    freq_by_year_y = [seeking.freq_1943, seeking.freq_1947, seeking.freq_1948, seeking.freq_1950, seeking.freq_1951, seeking.freq_1952,
                      seeking.freq_1953, seeking.freq_1954, seeking.freq_1955, seeking.freq_1956, seeking.freq_1957,
                      seeking.freq_1958, seeking.freq_1959, seeking.freq_1960, seeking.freq_1961, seeking.freq_1962,
                      seeking.freq_1963, seeking.freq_1964, seeking.freq_1965, seeking.freq_1966, seeking.freq_1967,
                      seeking.freq_1968, seeking.freq_1969, seeking.freq_1970]
    # film percentage                  
    collect_film = sum([seeking.freq_crime, seeking.freq_comedy, seeking.freq_drama])
    crime_percent = (seeking.freq_crime / collect_film) * 100
    comedy_percent = (seeking.freq_comedy / collect_film) * 100
    drama_percent = (seeking.freq_drama / collect_film) * 100

    # sex percentage
    collect_sex = sum([seeking.freq_female, seeking.freq_male])
    female_percent = (seeking.freq_female / collect_sex) * 100
    male_percent = (seeking.freq_male / collect_sex) * 100

    genre_crime = [seeking.freq_crime]
    genre_comedy = [seeking.freq_comedy]
    genre_drama = [seeking.freq_drama]
    female_sex = [seeking.freq_female]
    male_sex = [seeking.freq_male]

    # filter the details of sentence
    filtering = filters(request)
    sentence = Sentences.objects.all().exclude(tag='Pu')
    words = Words.objects.all().exclude(tag='Pu')
    next_url = ''
    prev_url = ''
    actors_id = []
    actors_gender = []
    actors_age = []

    films_id = []
    films_genre = []
    films_from = []
    films_to = []

    if request.method == "GET":
        try:
            if "query" in request.GET:
                request_query = request.GET.get('query', "")
                verb_option = request.GET.get("verb_option", "")
                formsets_option = request.GET.get("formsets_option", "contains")
                sentence = Sentences.objects.filter(annotation_string__contains="%s_%s_%s" % (slug, request.GET.get("verb_option", ""), request.GET.get("jyutping", "")))
        except:
            return redirect(f"{request.get_full_path()}&formsets_option=contains&verb_option=")
    s = sentence
    film_count = sentence.values_list('film_id').distinct().__len__()
    actor = request.GET.get('actor')
    gender = request.GET.get('gender')
    age = request.GET.get('age')

    film = request.GET.get('film')
    genre = request.GET.get('genre')
    fromm = request.GET.get('from')
    too = request.GET.get('to')

    actorr = None
    if actor and actor != 'all':
        actorr = Actors.objects.get(id=int(actor))

    genderr = None
    if gender and gender != 'all':
        genderr = gender

    agee = None
    if age and age != 'all':
        agee = age

    filmm = None
    if film and film != 'all':
        filmm = Films.objects.get(id=int(film))

    genree = None
    if genre and genre != 'all':
        genree = genre

    frommm = None
    if fromm and fromm != 'all':
        frommm = int(fromm)

    tooo = None
    if too and too != 'all':
        tooo = int(too)

    if "actor" in request.GET:
        if actor == 'all':
            actors = Actors.objects.all()
            sentence = sentence
        else:
            actors = Actors.objects.filter(id=int(actor))
            for act in actors:
                actors_id.append(Actors.objects.get(id=int(act.id)).id)
            sentence = sentence.filter(actor_id__in=actors_id)

        if gender == 'all':
            actors = actors
            sentence = sentence
        else:
            actors = actors.filter(gender=int(gender))
            for act in actors:
                actors_gender.append(Actors.objects.get(id=int(act.id)).id)
            sentence = sentence.filter(actor_id__in=actors_gender)

        if age == 'all':
            actors = actors
            sentence = sentence
        else:
            actors = actors.filter(age=int(age))
            for act in actors:
                actors_age.append(Actors.objects.get(id=int(act.id)).id)
            sentence = sentence.filter(actor_id__in=actors_age)

    if "film" in request.GET:
        if film == 'all':
            films = Films.objects.all()
            sentence = sentence
        else:
            films = Films.objects.filter(id=int(film))
            for film in films:
                films_id.append(Films.objects.get(id=int(film.id)).id)
            sentence = sentence.filter(film_id__in=films_id)

        if genre == 'all':
            films = films
            sentence = sentence
        else:
            films = films.filter(genre=int(genre))
            for film in films:
                films_genre.append(Films.objects.get(id=int(film.id)).id)
            sentence = sentence.filter(film_id__in=films_genre)

        if fromm == 'all':
            films = films
            sentence = sentence
        else:
            films = films.filter(year__gte=int(fromm))
            for film in films:
                films_from.append(Films.objects.get(id=int(film.id)).id)
            sentence = sentence.filter(film_id__in=films_from)

        if too == 'all':
            films = films
            sentence = sentence
        else:
            films = films.filter(year__lte=int(too))
            for film in films:
                films_to.append(Films.objects.get(id=int(film.id)).id)
            sentence = sentence.filter(film_id__in=films_to)

    if sentence:
        paginator = Paginator(sentence, 20)
        page_number = request.GET.get('page_number')
        sentence = paginator.get_page(page_number)
        if sentence.has_next():
            next_url = f"{request.get_raw_uri()}&page_number={sentence.next_page_number()}"
        else:
            next_url = ''

        if sentence.has_previous():
            prev_url = f"{request.get_raw_uri()}&page_number={sentence.previous_page_number()}"
        else:
            prev_url = ''

    if words:
        paginator = Paginator(words, 50)
        page_number = request.GET.get('page_numberr')
        words = paginator.get_page(page_number)

    word_orth = Words.objects.get(id=word_id)
    context = {
        "sentence_count": s,
        "word_details": word_orth,
        "freq_by_year_x": freq_by_year_x,
        "freq_by_year_y": freq_by_year_y,
        "genre_crime": genre_crime,
        "genre_comedy": genre_comedy,
        "genre_drama": genre_drama,
        "female_sex": female_sex,
        "male_sex": male_sex,
        "token": token,
        "crime_percent": crime_percent,
        "comedy_percent": comedy_percent,
        "drama_percent": drama_percent,
        "female_percent": female_percent,
        "male_percent": male_percent,
        'sentences': sentence,
        'words': words,
        'filter': filtering,
        'verb_option': request.GET.get("verb_option", word_orth.pron),
        'formsets_option': request.GET.get("formsets_option", "contains"),
        'actorr': actorr,
        'genderr': genderr,
        'agee': agee,
        'filmm': filmm,
        'genree': genree,
        'frommm': frommm,
        'tooo': tooo,
        'next_url': next_url,
        'prev_url': prev_url,
        'from_to_year': Films.objects.all().order_by('year').values_list('year', flat=True).distinct(),
        'word_orth': word_orth,
        'film_count': film_count
    }
    return render(request, 'search/details.html', context)
