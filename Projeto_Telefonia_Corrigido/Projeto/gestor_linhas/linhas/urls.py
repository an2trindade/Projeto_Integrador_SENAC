from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_linhas, name="lista_linhas"),
    path("nova/", views.nova_linha, name="nova_linha"),
    path("editar/<int:pk>/", views.editar_linha, name="editar_linha"),
    path("excluir/<int:pk>/", views.excluir_linha, name="excluir_linha"),
    path("detalhes/<int:pk>/", views.detalhes_linha, name="detalhes_linha"),
]