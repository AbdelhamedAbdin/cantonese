import datetime
from django.shortcuts import render, redirect
from .forms import (RegisterForm, AuthenticationForm, PasswordResetForm,
                    CustomPasswordChangeForm)
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from .models import User, Profile, History
from django.core.mail import EmailMessage, send_mail
from django.views.generic import View
from django.utils.encoding import force_text, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utiliz import token_generator
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView as password_view
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.views import PasswordResetDoneView
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from website import settings
from django.template import loader
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django import template
from django.contrib.auth.tokens import default_token_generator
from django.core import serializers
from .custom_decorator import decoratorDirect
import re


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)

        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            try:
                usr = User.objects.get(email=data)
            except User.DoesNotExist:
                messages.error(request, "%s Does not exists" % data, extra_tags='user_error')
                return redirect('accounts:reset_password')
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    plaintext = template.loader.get_template('accounts/password_reset_subject.txt')
                    htmltemp = template.loader.get_template('accounts/password_reset_email.html')
                    c = {
                    "email": user.email,
                    'domain': '127.0.0.1:8000',
                    'site_name': 'Corpus',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    text_content = plaintext.render(c)
                    html_content = htmltemp.render(c)
                    try:
                        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [user.email], headers={'Reply-To': 'admin@example.com'})
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.info(request, "Password reset instructions have been sent to the email address entered.")
                return redirect("accounts:password_reset_done")
    password_reset_form = PasswordResetForm(None)
    return render(request=request, template_name="accounts/password_reset_form.html", context={"form": password_reset_form})


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordChangeView(password_view):
    form_class = CustomPasswordChangeForm
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy("index:home")


# Register
def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                email=form.cleaned_data['email'],
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password']
            )
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse('accounts:activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})

            activate_url = request.scheme+"://%s%s" % (domain, link)
            email_subject = 'Activate your account'
            email_body = 'Hi %s please use this link to verify your account\n%s' % (user.username, activate_url)
            email_message = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [user]
            )
            email_message.send(fail_silently=False)
            messages.success(request, 'Account successful created, please verify your account.',
                           extra_tags='register_success')
            return redirect('accounts:login')
    else:
        form = RegisterForm(None)
    return render(request, 'accounts/register.html', {'form': form})


def func(n):
    return n

# Profile page
@login_required
@decoratorDirect
def userProfile(request, slug=None):
    profile = Profile.objects.get(user__slug=slug)
    history = profile.user.user_history.all()
    users = User.objects.all()
    all_history = History.objects.all()
    next_url = None
    prev_url = None
    formsets_option = ''
    verb_option = ''
    user = request.GET.get('user')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    adv_search = request.GET.get('advanced_search', 0)
    userr = None
    select_history = None
    request_query = None
    user_list = []
    date_list = []
    all_users = None

    if user and user != 'all':
        userr = User.objects.get(username=user)

    if "user" in request.GET:
        if user == 'all':
            all_users = users
            all_history = all_history
        else:
            all_users = User.objects.filter(username=user)
            for u in all_users:
                user_list.append(User.objects.get(id=int(u.id)).id)
            all_history = all_history.filter(user__in=user_list)

        for x in all_users:
            for u in x.user_history.all():
                date_list.append(all_history.get(id=u.id).history_time)
        select_history = all_history.filter(history_time__in=date_list)  # date based on User

        if start_date:
            START_DATE = all_history.filter(history_time__gte=str(start_date).strip(" "))
            date_list = []

            for d in START_DATE:
                date_list.append(d.history_time)
            all_history = all_history.filter(history_time__in=date_list)

        if end_date:
            if start_date:
                END_DATE = all_history.filter(history_time__lte=str(end_date).strip(" ")).filter(history_time__gte=str(start_date).strip(" "))
            else:
                END_DATE = all_history.filter(history_time__exact=str(end_date).strip(" "))
            date_list = []

            for d in END_DATE:
                date_list.append(d.history_time)
            all_history = all_history.filter(history_time__in=date_list)

    if 'advanced_search' in request.GET:
        if request.user.is_superuser:
            if adv_search == '0':
                all_history = all_history
            elif adv_search == '1':
                all_history = all_history.exclude(advanced_search=True)
            elif adv_search == '2':
                all_history = all_history.filter(advanced_search=True).exclude(advanced_search=False)
        else:
            if adv_search == '0':
                history = history
            elif adv_search == '1':
                history = history.exclude(advanced_search=True)
            elif adv_search == '2':
                history = history.filter(advanced_search=True).exclude(advanced_search=False)

    try:
        if "query" in request.GET:
            if request.GET['query'] != "":
                request_query = request.GET.get('query')
                verb_option = request.GET.get("verb_option")
                formsets_option = request.GET['formsets_option']
                if verb_option == "":
                    v = "POS"
                else:
                    v = verb_option

                if History.objects.filter(
                    history=request_query,
                    verb_option=v,
                    action_option=formsets_option
                ).exists():
                    History.objects.create(
                        user=User.objects.get(username=slug),
                        history=request_query,
                        verb_option=v,
                        action_option=formsets_option,
                        advanced_search=True
                    )

                if request.GET['formsets_option'] == "contains":
                    if v != 'POS':
                        if not request.user.is_superuser:
                            history = history.filter(
                                Q(history__contains=request_query) |
                                Q(history_time__contains=request_query)
                            ).filter(verb_option__contains=verb_option).filter(action_option__contains=formsets_option)
                        else:
                            all_history = all_history.filter(
                                Q(history__contains=request_query) |
                                Q(history_time__contains=request_query)
                            ).filter(verb_option__contains=verb_option).filter(action_option__contains=formsets_option)
                    else:
                        if not request.user.is_superuser:
                            history = history.filter(
                                Q(history__contains=request_query) |
                                Q(history_time__contains=request_query)
                            ).filter(action_option__contains=formsets_option)
                        else:
                            all_history = all_history.filter(
                                Q(history__contains=request_query) |
                                Q(history_time__contains=request_query)
                            ).filter(action_option__contains=formsets_option)
                elif request.GET['formsets_option'] == "is":
                    if v != 'POS':
                        if not request.user.is_superuser:
                            history = history.filter(
                                Q(history__contains=request_query) |
                                Q(history_time__contains=request_query)
                            ).filter(verb_option__contains=verb_option).filter(action_option__contains=formsets_option)
                        else:
                            all_history = all_history.filter(
                                Q(history__contains=request_query) |
                                Q(history_time__contains=request_query)
                            ).filter(verb_option__contains=verb_option).filter(action_option__contains=formsets_option)
                    else:
                        if not request.user.is_superuser:
                            history = history.filter(
                                Q(history__contains=request_query) |
                                Q(history_time__contains=request_query)
                            ).filter(action_option__contains=formsets_option)
                        else:
                            all_history = all_history.filter(
                                Q(history__contains=request_query) |
                                Q(history_time__contains=request_query)
                            ).filter(action_option__contains=formsets_option)
                elif request.GET['formsets_option'] == "start_with":
                    if v != 'POS':
                        if not request.user.is_superuser:
                            history = history.filter(
                                Q(history__contains=request_query) |
                                Q(history_time__contains=request_query)
                            ).filter(verb_option__contains=verb_option).filter(action_option__contains=formsets_option)
                        else:
                            all_history = all_history.filter(
                                Q(history__contains=request_query) |
                                Q(history_time__contains=request_query)
                            ).filter(verb_option__contains=verb_option).filter(action_option__contains=formsets_option)
                    else:
                        if not request.user.is_superuser:
                            history = history.filter(
                                Q(history__contains=request_query) |
                                Q(history_time__contains=request_query)
                            ).filter(action_option__contains=formsets_option)
                        else:
                            all_history = all_history.filter(
                                Q(history__contains=request_query) |
                                Q(history_time__contains=request_query)
                            ).filter(action_option__contains=formsets_option)

                elif request.GET['formsets_option'] == "end_with":
                    if v != 'POS':
                        if not request.user.is_superuser:
                            history = history.filter(
                                Q(history__contains=request_query) |
                                Q(history_time__contains=request_query)
                            ).filter(verb_option__contains=verb_option).filter(action_option__contains=formsets_option)
                        else:
                            all_history = all_history.filter(
                                Q(history__contains=request_query) |
                                Q(history_time__contains=request_query)
                            ).filter(verb_option__contains=verb_option).filter(action_option__contains=formsets_option)
                    else:
                        if not request.user.is_superuser:
                            history = history.filter(
                                Q(history__contains=request_query) |
                                Q(history_time__contains=request_query)
                            ).filter(action_option__contains=formsets_option)
                        else:
                            all_history = all_history.filter(
                                Q(history__contains=request_query) |
                                Q(history_time__contains=request_query)
                            ).filter(action_option__contains=formsets_option)

        history = history.filter(deleted_history=False)

        if history:
            paginator = Paginator(history, 100)
            page_number = request.GET.get('page_number')
            history = paginator.get_page(page_number)

            if history.has_next():
                next_url = f"{request.get_raw_uri()}&page_number={history.next_page_number()}"
            else:
                next_url = ''

            if history.has_previous():
                prev_url = f"{request.get_raw_uri()}&page_number={history.previous_page_number()}"
            else:
                prev_url = ''

        if all_history:
            paginator = Paginator(all_history, 100)
            page_number = request.GET.get('page_number')
            all_history = paginator.get_page(page_number)

            if all_history.has_next():
                next_url = f"{request.get_raw_uri()}&page_number={all_history.next_page_number()}"
            else:
                next_url = ''

            if all_history.has_previous():
                prev_url = f"{request.get_raw_uri()}&page_number={all_history.previous_page_number()}"
            else:
                prev_url = ''
    except:
        return redirect('accounts:index_404')

    context = {
        'profile': profile,
        'history_pages': history,
        'next_url': next_url,
        'prev_url': prev_url,
        'formsets_option': formsets_option,
        'query': request_query,
        'verb_option': verb_option,
        'users': users,
        'all_history': all_history,
        'userr': userr,
        'my_user': user,
        'select_history': select_history,
        'adv_search': adv_search
    }
    return render(request, 'accounts/profile.html', context, status=200)


def superuser_history(request):
    if ('remove_multiple_items' and 'remove_one_item') not in request.POST:
        if 'remove_one_item' in request.POST:
            h = History.objects.get(id=int(request.POST.get('remove_one_item')))
            h.delete()
        elif 'remove_multiple_items' in request.POST:
            for items in request.POST.getlist('remove_multiple_items'):
                h = History.objects.get(id=int(items))
                h.delete()
    return redirect(reverse('accounts:profile', args=[request.user.username]))


def compileFunction(pattern, string):
    re_obj = re.compile(pattern)
    return re_obj.findall(string)


def query_iter(args):
    for arg in args:
        yield 'query=%s' % str(arg)


def verb_iter(args):
    for arg in args:
        if arg == 'POS':
            arg = ""
        yield 'verb_option=%s' % str(arg)


def formsets_iter(args):
    for arg in args:
        yield 'formsets_option=%s' % str(arg)


# redo to main page & create a history advanced
def redo_main_history(request):
    if 'to_main_history' in request.POST:
        query_obj = compileFunction("[\u4e00-\u9fff]+|[？]|[。]|[，]|[…]|[！]|[a-zA-Z0-9]+", str(request.POST.getlist('query')))
        verb_option_obj = compileFunction("[a-zA-Z]+", str(request.POST.getlist('verb_option')))
        formsets_option_obj = compileFunction("[a-zA-Z_]+", str(request.POST.getlist('formsets_option')))
        query_string = ""
        verb_string = ""
        formsets_string = ""

        for query in query_iter(query_obj):
            query_string += query + '&'

        for verb in verb_iter(verb_option_obj):
            verb_string += verb + "&"

        for formsets in formsets_iter(formsets_option_obj):
            formsets_string += formsets + '&'

        format_query_string = '''/v2/search/find/?{query}{verb}{formsets}'''
        format_query_string = format_query_string.format(query=query_string,
                                 verb=verb_string,
                                 formsets=formsets_string)
        return redirect(format_query_string.rstrip("&"))
    return redirect(reverse('accounts:profile', args=[request.user.username]))


def normal_user(request):
    if ('remove_multiple_items' and 'remove_one_item') not in request.POST:
        if 'remove_one_item' in request.POST:
            h = History.objects.get(id=int(request.POST.get('remove_one_item')))
            h.deleted_history = True
            h.save()
        elif 'remove_multiple_items' in request.POST:
            for items in request.POST.getlist('remove_multiple_items'):
                h = History.objects.get(id=int(items))
                h.deleted_history = True
                h.save()
        elif 'test' in request.POST:
            print('test for normal user')
    return redirect(reverse('accounts:profile', args=[request.user.username]) + '?page_number=1&advanced_search=0')


def page_not_found(request):
    context = {'obj': request}
    return render(request, 'accounts/index_404.html', context)


def change_name(request):
    if request.method == 'POST':
        FirstNameForm = request.POST['first_name']
        LastNameForm = request.POST['last_name']
        if FirstNameForm and FirstNameForm != None:
            user = User.objects.get(username=request.user.username)
            user.first_name = FirstNameForm
            user.save()

        if LastNameForm and LastNameForm != None:
            user = User.objects.get(username=request.user.username)
            user.last_name = LastNameForm
            user.save()

        return redirect(reverse('accounts:profile', args=[request.user.username]))
    return render(request, 'accounts/change_name.html', {})


# login
def Login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.user_signed == False:
                    messages.error(request, 'you have to confirm your mail first', extra_tags='not_confirmed')
                    return redirect("accounts:login")
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('accounts:profile', args=[request.user.username]) + '?page_number=1&advanced_search=0')
            else:
                messages.error(request, 'email or password are invalid. please try again.', extra_tags='validate_form')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', context={'form': form})


# Logout
class Logout(LogoutView):
    template_name = 'accounts/logout.html'
    next_page = reverse_lazy('accounts:login')


class Verification(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not token_generator.check_token(user, token):
                return redirect('accounts:login')

            if user.is_active:
                user.user_signed = True
                user.save()
                return redirect('accounts:login')
            user.is_active = True
            user.save()

            messages.success(request, "Account activated successfully", extra_tags='register_success')
            return redirect('accounts:login_success')
        except:
            pass


def get_date_by_name(request):
    pass
