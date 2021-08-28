from django.urls import path, re_path
from . import views
import urllib
from django.utils.http import urlquote

app_name = "search"

urlpatterns = [
    path("find/", views.search, name="search"),
    re_path(u"search-details/(?P<slug>[\u4e00-\u9fff]+|[？]|[。]|[，]|[…]|[！]|[㖡]|[a-zA-Z0-9]+|[𠻹]|[㗎]|[𡃇]|[>]|[(a-zA-Z0-9)]+|[𠺬]|[^]]|[^[]|[𡁻]|[㧬]|[㓤]|[\u4e00-\u9fffa-zA-Z0-9]+|[𠺘]|[?|\\//!@#$%^&*()~`]+)/", views.search_details, name="details")
]
