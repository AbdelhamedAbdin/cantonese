from django.http import HttpResponseRedirect


def decoratorDirect(func):
    def wrapper(request, slug):
        if request.path == '/accounts/profile/' + request.user.slug + '/' and request.GET == {}:
            if 'page_number' not in request.GET:
                return HttpResponseRedirect('/accounts/profile/' + request.user.slug + '?page_number=1&advanced_search=0')
        return func(request, slug)
    return wrapper
