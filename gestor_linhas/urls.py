from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings


class CustomLoginView(LoginView):
    """Custom LoginView that always redirects to LOGIN_REDIRECT_URL regardless of 'next' param."""
    def get_success_url(self):
        # Always return the configured LOGIN_REDIRECT_URL
        return settings.LOGIN_REDIRECT_URL

urlpatterns = [
    path("admin/", admin.site.urls),
    path("linhas/", include(("linhas.urls", "linhas"), namespace="linhas")),
    path("api/", include("linhas.api_urls")),
    path("login/", CustomLoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="/login/"), name="logout"),
    path("", RedirectView.as_view(url="/linhas/listalinhas/", permanent=False)),
]


