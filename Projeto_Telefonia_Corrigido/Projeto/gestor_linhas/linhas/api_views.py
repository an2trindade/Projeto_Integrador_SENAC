from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Count, Q
from .models import Linha
from .serializers import LinhaSerializer, LinhaCreateSerializer, EstatisticasSerializer

class LinhaListCreateView(generics.ListCreateAPIView):
    """
    Lista todas as linhas de telefonia ou cria uma nova linha
    """
    queryset = Linha.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LinhaCreateSerializer
        return LinhaSerializer
    
    def get_queryset(self):
        queryset = Linha.objects.all()
        
        # Filtros opcionais
        operadora = self.request.query_params.get('operadora')
        tipo_plano = self.request.query_params.get('tipo_plano')
        ativa = self.request.query_params.get('ativa')
        busca = self.request.query_params.get('busca')
        
        if operadora:
            queryset = queryset.filter(operadora=operadora)
        
        if tipo_plano:
            queryset = queryset.filter(tipo_plano=tipo_plano)
        
        if ativa is not None:
            queryset = queryset.filter(ativa=ativa.lower() == 'true')
        
        if busca:
            queryset = queryset.filter(
                Q(numero__icontains=busca) |
                Q(nome_titular__icontains=busca) |
                Q(operadora__icontains=busca)
            )
        
        return queryset.order_by('-criado_em')
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)

class LinhaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Recupera, atualiza ou deleta uma linha específica
    """
    queryset = Linha.objects.all()
    serializer_class = LinhaSerializer
    permission_classes = [IsAuthenticated]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def estatisticas_view(request):
    """
    Retorna estatísticas gerais do sistema de linhas
    """
    linhas = Linha.objects.all()
    
    # Estatísticas básicas
    total_linhas = linhas.count()
    linhas_ativas = linhas.filter(ativa=True).count()
    linhas_inativas = linhas.filter(ativa=False).count()
    
    # Valor total dos planos
    total_valor_planos = linhas.aggregate(
        total=Sum('valor_plano')
    )['total'] or 0
    
    # Contagem por operadora
    operadoras_count = {}
    for operadora_key, operadora_nome in Linha.OPERADORA_CHOICES:
        count = linhas.filter(operadora=operadora_key).count()
        if count > 0:
            operadoras_count[operadora_nome] = count
    
    # Contagem por tipo de plano
    tipos_plano_count = {}
    for tipo_key, tipo_nome in Linha.TIPO_CHOICES:
        count = linhas.filter(tipo_plano=tipo_key).count()
        if count > 0:
            tipos_plano_count[tipo_nome] = count
    
    dados = {
        'total_linhas': total_linhas,
        'linhas_ativas': linhas_ativas,
        'linhas_inativas': linhas_inativas,
        'total_valor_planos': total_valor_planos,
        'operadoras_count': operadoras_count,
        'tipos_plano_count': tipos_plano_count,
    }
    
    serializer = EstatisticasSerializer(dados)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ativar_desativar_linha(request, pk):
    """
    Ativa ou desativa uma linha específica
    """
    try:
        linha = Linha.objects.get(pk=pk)
    except Linha.DoesNotExist:
        return Response(
            {'erro': 'Linha não encontrada'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    acao = request.data.get('acao')
    
    if acao == 'ativar':
        linha.ativa = True
        mensagem = f'Linha {linha.numero} ativada com sucesso'
    elif acao == 'desativar':
        linha.ativa = False
        mensagem = f'Linha {linha.numero} desativada com sucesso'
    else:
        return Response(
            {'erro': 'Ação inválida. Use "ativar" ou "desativar"'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    linha.save()
    
    serializer = LinhaSerializer(linha)
    return Response({
        'mensagem': mensagem,
        'linha': serializer.data
    })

