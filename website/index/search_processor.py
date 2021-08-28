from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator
from list_app.models import Words, Sentences, Films, Characters, Actors


def main_search(request):
    if request.user.is_authenticated:
        if "query" in request.GET:
            request_query = request.GET.get("query", "")
            sentence = Sentences.objects.all()
            request.GET.get('formsets_option', "contains")
            request.GET.get("verb_option", "Pron")
            sentence.filter(
                Q(orth__contains=request_query) |
                Q(tag__contains=request_query) |
                Q(pron__contains=request_query)
            ).exclude(tag__contains='Pu')

            paginator = Paginator(sentence, 20)
            page_number = request.GET.get('page_number')
            sentence = paginator.get_page(page_number)
            url = f"v2/search/find/?formsets_option=contains&query={request.GET['query']}&verb_option=&main_search=Search"
            return request
            # return {'url': url}
    else:
        return {}
    # return render(request, 'index/home.html', {})
