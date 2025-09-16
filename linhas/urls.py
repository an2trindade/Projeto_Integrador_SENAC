from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path("", RedirectView.as_view(url="listalinhas/", permanent=False)),
    path("listalinhas/", views.lista_linhas, name="listalinhas"),
    path("nova/", views.nova_linha, name="novalinha"),
    path("editar/<int:pk>/", views.editar_linha, name="editarlinha"),
    path("excluir/<int:pk>/", views.excluir_linha, name="excluirlinha"),
    path("detalhes/<int:pk>/", views.detalhes_linha, name="detalheslinha"),
    path("buscar-linhas-estoque/", views.buscar_linhas_estoque, name="buscar_linhas_estoque"),
    path("buscar-cliente-cnpj/", views.buscar_cliente_por_cnpj, name="buscar_cliente_por_cnpj"),
    path("autocomplete-cnpj/", views.autocomplete_cnpj, name="autocomplete_cnpj"),
    path("listar-rps-cliente/", views.listar_rps_cliente, name="listar_rps_cliente"),
]