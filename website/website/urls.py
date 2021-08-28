from django.contrib import admin
from django.urls import path, include, re_path
from django.urls import reverse_lazy
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth.views import PasswordResetConfirmView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('index.urls')),
    path('v2/introduction/', include('introduction.urls')),
    path('v2/search/', include('corpus_search.urls')),
    path('v2/', include('list_app.urls')),
    path('accounts/', include('accounts.urls'))
]

urlpatterns += i18n_patterns(
    path('password-reset-confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html',
                                         success_url=reverse_lazy('accounts:password_reset_complete')),
                                         name='password_reset_confirm'),
)
