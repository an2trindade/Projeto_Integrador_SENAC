from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path("", RedirectView.as_view(url="login/", permanent=False)),
    path("login/", views.login_view, name="login"),
    path("listalinhas/", views.lista_linhas, name="listalinhas"),
    path("nova/", views.nova_linha, name="novalinha"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("protocolo/", views.protocolo, name="protocolo"),
    path("relatorios/", views.relatorios, name="relatorios"),
    path("clientes/novo/", views.cliente_novo, name="cliente_novo"),
    path("clientes/novo-ajax/", views.cliente_create_ajax, name="cliente_create_ajax"),
    path("relatorios/export/linhas-cycle/", views.export_linhas_cycle_csv, name="export_linhas_cycle_csv"),
    path("relatorios/export/linhas-cycle-xlsx/", views.export_linhas_cycle_xlsx, name="export_linhas_cycle_xlsx"),
    path("relatorios/export/protocolos-pendentes/", views.export_protocolos_pendentes_csv, name="export_protocolos_pendentes_csv"),
    path("configuracoes/", views.configuracoes, name="configuracoes"),
    path("editar/<int:pk>/", views.editar_linha, name="editarlinha"),
    path("excluir/<int:pk>/", views.excluir_linha, name="excluirlinha"),
    path("detalhes/<int:pk>/", views.detalhes_linha, name="detalheslinha"),
    path("buscar-linhas-estoque/", views.buscar_linhas_estoque, name="buscar_linhas_estoque"),
    path("buscar-cliente-cnpj/", views.buscar_cliente_por_cnpj, name="buscar_cliente_por_cnpj"),
    path("buscar-cnpj-api/", views.buscar_cnpj_api_externa, name="buscar_cnpj_api_externa"),
    path("test-cnpj-api/", views.test_cnpj_api_view, name="test_cnpj_api"),
    path("debug-cnpj-button/", views.debug_cnpj_button_view, name="debug_cnpj_button"),
    path("buscar-empresas/", views.buscar_empresas, name="buscar_empresas"),
    path("buscar-clientes/", views.buscar_clientes, name="buscar_clientes"),
    path("autocomplete-cnpj/", views.autocomplete_cnpj, name="autocomplete_cnpj"),
    path("listar-rps-cliente/", views.listar_rps_cliente, name="listar_rps_cliente"),
]