from django.urls import path
from . import api_views

urlpatterns = [
    path('linhas/', api_views.LinhaListCreateView.as_view(), name='api_linhas_list'),
    path('linhas/<int:pk>/', api_views.LinhaDetailView.as_view(), name='api_linha_detail'),
    path('linhas/<int:pk>/ativar-desativar/', api_views.ativar_desativar_linha, name='api_linha_ativar_desativar'),
    path('estatisticas/', api_views.estatisticas_view, name='api_estatisticas'),
]

