from django.urls import path, re_path
from . import views
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth import views as auth_views

app_name = 'accounts'


urlpatterns = [
    path('profile/<slug:slug>/', views.userProfile, name="profile"),
    path('register/', views.register, name="register"),
    path('login/', views.Login, name='login'),
    path('remove-history/', views.superuser_history, name='remove_history'),
    path('redo-to-main-history/', views.redo_main_history, name='redo_to_main_history'),
    path('remove-multiple-history/', views.normal_user, name='remove_multiple_history'),
    path('page-not-found/', views.page_not_found, name='index_404'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path("activate/<uidb64>/<token>/", views.Verification.as_view(), name="activate"),
    path("change-password/", views.PasswordChangeView.as_view(), name="change_password"),
    path("change-name/", views.change_name, name="change_name"),
    # forgot password links
    path('password_reset/', views.password_reset_request, name='reset_password'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), name='password_reset_done'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name='password_reset_complete'),

]
