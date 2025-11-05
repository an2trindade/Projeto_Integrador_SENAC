from django.contrib import admin
from .models import Linha
from .models import Protocolo
from .models import Cliente

@admin.register(Linha)
class LinhaAdmin(admin.ModelAdmin):
    list_display = [
        'numero', 'iccid', 'acao', 'cnpj', 'empresa', 'rp', 'tipo_plano',
        'valor_plano', 'taxa_manutencao', 'ativa', 'criado_em'
    ]
    list_filter = [
        'acao', 'tipo_plano', 'ativa', 'criado_em'
    ]
    search_fields = [
        'numero', 'iccid', 'acao', 'cnpj', 'empresa', 'rp'
    ]
    list_editable = ['ativa']
    list_per_page = 25
    date_hierarchy = 'criado_em'

    fieldsets = (
        ('Informações da Linha', {
            'fields': ('numero', 'iccid', 'acao', 'cnpj', 'empresa', 'rp')
        }),
        ('Plano', {
            'fields': ('tipo_plano', 'valor_plano', 'taxa_manutencao')
        }),
        ('Status e Observações', {
            'fields': ('ativa', 'observacoes')
        }),
        ('Metadados', {
            'fields': ('criado_por', 'criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['criado_em', 'atualizado_em']
    
    def save_model(self, request, obj, form, change):
        if not change:  # Se é um novo objeto
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('criado_por')
    
    # Ações personalizadas
    actions = ['ativar_linhas', 'desativar_linhas']
    
    def ativar_linhas(self, request, queryset):
        count = queryset.update(ativa=True)
        self.message_user(request, f'{count} linha(s) ativada(s) com sucesso.')
    ativar_linhas.short_description = 'Ativar linhas selecionadas'
    
    def desativar_linhas(self, request, queryset):
        count = queryset.update(ativa=False)
        self.message_user(request, f'{count} linha(s) desativada(s) com sucesso.')
    desativar_linhas.short_description = 'Desativar linhas selecionadas'


@admin.register(Protocolo)
class ProtocoloAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'status', 'criado_por', 'criado_em']
    list_filter = ['status', 'criado_em']
    search_fields = ['titulo', 'descricao']
    readonly_fields = ['criado_em']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'cnpj', 'contato', 'telefone')
    search_fields = ('empresa', 'cnpj', 'contato')

