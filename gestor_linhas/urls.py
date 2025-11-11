from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("linhas/", include(("linhas.urls", "linhas"), namespace="linhas")),
    path("api/", include("linhas.api_urls")),
    # Redirect antigo /login/ para novo /linhas/login/
    path("login/", RedirectView.as_view(url="/linhas/login/", permanent=True)),
    path("logout/", LogoutView.as_view(next_page="/linhas/login/"), name="logout"),
    path("", RedirectView.as_view(url="/linhas/login/", permanent=False)),
]


