from rest_framework import serializers
from .models import Linha

class LinhaSerializer(serializers.ModelSerializer):
    operadora_display = serializers.CharField(source='get_operadora_display', read_only=True)
    tipo_plano_display = serializers.CharField(source='get_tipo_plano_display', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.username', read_only=True)
    
    class Meta:
        model = Linha
        fields = [
            'id', 'numero', 'nome_titular', 'operadora', 'operadora_display',
            'tipo_plano', 'tipo_plano_display', 'valor_plano', 'data_contratacao',
            'data_vencimento', 'ativa', 'observacoes', 'criado_por', 'criado_por_nome',
            'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['id', 'criado_por', 'criado_em', 'atualizado_em']

    def validate_numero(self, value):
        """Valida o formato do número de telefone"""
        # Remove caracteres não numéricos
        numero_limpo = ''.join(filter(str.isdigit, value))
        
        if len(numero_limpo) < 10 or len(numero_limpo) > 11:
            raise serializers.ValidationError('Número deve ter 10 ou 11 dígitos.')
        
        # Verifica se já existe outro registro com o mesmo número
        instance_id = self.instance.id if self.instance else None
        if Linha.objects.filter(numero=value).exclude(id=instance_id).exists():
            raise serializers.ValidationError('Já existe uma linha com este número.')
        
        return value

    def validate_valor_plano(self, value):
        """Valida se o valor do plano é positivo"""
        if value <= 0:
            raise serializers.ValidationError('O valor do plano deve ser maior que zero.')
        return value

class LinhaCreateSerializer(serializers.ModelSerializer):
    """Serializer específico para criação de linhas"""
    class Meta:
        model = Linha
        fields = [
            'numero', 'nome_titular', 'operadora', 'tipo_plano', 
            'valor_plano', 'data_contratacao', 'data_vencimento', 
            'ativa', 'observacoes'
        ]

    def validate_numero(self, value):
        """Valida o formato do número de telefone"""
        numero_limpo = ''.join(filter(str.isdigit, value))
        
        if len(numero_limpo) < 10 or len(numero_limpo) > 11:
            raise serializers.ValidationError('Número deve ter 10 ou 11 dígitos.')
        
        if Linha.objects.filter(numero=value).exists():
            raise serializers.ValidationError('Já existe uma linha com este número.')
        
        return value

    def validate_valor_plano(self, value):
        """Valida se o valor do plano é positivo"""
        if value <= 0:
            raise serializers.ValidationError('O valor do plano deve ser maior que zero.')
        return value

class EstatisticasSerializer(serializers.Serializer):
    """Serializer para estatísticas do sistema"""
    total_linhas = serializers.IntegerField()
    linhas_ativas = serializers.IntegerField()
    linhas_inativas = serializers.IntegerField()
    total_valor_planos = serializers.DecimalField(max_digits=12, decimal_places=2)
    operadoras_count = serializers.DictField()
    tipos_plano_count = serializers.DictField()

