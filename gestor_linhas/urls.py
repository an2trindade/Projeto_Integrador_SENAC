from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("linhas/", include(("linhas.urls", "linhas"), namespace="linhas")),
    path("api/", include("linhas.api_urls")),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="/login/"), name="logout"),
    path("", RedirectView.as_view(url="/linhas/listalinhas/", permanent=False)),
]


