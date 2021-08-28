from django.shortcuts import render, redirect, reverse
from .models import Words, Films, Characters, Actors


def listWords(request):
    words = Words.objects.all().exclude(tag='Pu')
    summation = sum(words.values_list('freq', flat=True))
    if 'query' in request.GET:
        return redirect(f'/v2/search/find/search/search-details/{request.GET.get("query")}/?query={request.GET.get("query")}&formsets_option=contains&verb_option={request.GET.get("verb_option")}&jyutping={request.GET.get("jyutping")}')

    orth_list = []
    pron_list = []
    tag_list = []
    freq_list = []
    percentage = []
    counter = 0
    while counter < 100:
        percent_num = (words[counter].freq / summation) * 100
        percentage.append(percent_num)
        orth_list.append(words.values_list('orth', flat=True)[counter])
        pron_list.append(words.values_list('pron', flat=True)[counter])
        tag_list.append(words.values_list('tag', flat=True)[counter])
        freq_list.append(words.values_list('freq', flat=True)[counter])
        counter += 1      

    cum_list = []
    counter = 0
    inc = 0
    while counter < 100:
        inc += percentage[counter]
        cum_list.append(inc)
        counter += 1

    context = zip(orth_list, pron_list, tag_list, freq_list, percentage, cum_list)    

    context = {
        "context": context
    }
    return render(request, 'list_app/words.html', context)


def listCharacters(request):
    chars = Characters.objects.all()
    summation = sum(chars.values_list('freq', flat=True))
    if 'query' in request.GET:
        return redirect(f'/v2/search/find/search/search-details/{request.GET.get("query")}/?query={request.GET.get("query")}&formsets_option=contains&verb_option=')

    char_list = []
    freq_list = []
    percentage = []
    counter = 0
    while counter < 100:
        percent_num = (chars[counter].freq / summation) * 100
        percentage.append(percent_num)
        char_list.append(chars.values_list('character', flat=True)[counter])
        freq_list.append(chars.values_list('freq', flat=True)[counter])
        counter += 1      

    cum_list = []
    counter = 0
    inc = 0
    while counter < 100:
        inc += percentage[counter]
        cum_list.append(inc)
        counter += 1

    context = zip(char_list, freq_list, percentage, cum_list)

    context = {
        "context": context
    }
    return render(request, 'list_app/char.html', context)


def listActors(request):
    actors = Actors.objects.all()
    context = {
        'actors': enumerate(actors),
        'pages': actors
    }
    return render(request, 'list_app/actors.html', context)


def listFilms(request):
    films = Films.objects.all()
    context = {
        'films': enumerate(films),
        'pages': films
    }
    return render(request, 'list_app/films.html', context)
