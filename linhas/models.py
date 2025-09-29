from django.db import models
from django.contrib.auth.models import User

class Linha(models.Model):
    TIPO_CHOICES = [
        ('BLACK_VOZ_GW_800SMS', 'BLACK VOZ + GW + 800SMS'),
        ('BLACK_1GB_GW_800SMS', 'BLACK 1GB + GW + 800SMS'),
        ('BLACK_5GB_GW_800SMS', 'BLACK 5GB + GW + 800SMS = CONT. MENSAGEM + MOBILIDADE + REDE SOCIAL'),
        ('BLACK_10GB_GW_800SMS', 'BLACK 10GB + GW + 800SMS = CONT. MENSAGEM + MOBILIDADE + REDE SOCIAL'),
        ('BLACK_20GB_GW_800SMS', 'BLACK 20GB + GW + 800SMS = CONT. MENSAGEM + MOBILIDADE + REDE SOCIAL'),
        ('BLACK_50GB_GW_800SMS', 'BLACK 50GB + GW + 800SMS = CONT. MENSAGEM + MOBILIDADE + REDE SOCIAL'),
        ('BLACK_ILIMITADO_GB_GW_800SMS', 'BLACK ILIMITADO GB + GW + 800SMS = CONT. MENSAGEM + MOBILIDADE + REDE SOCIAL'),
    ]
    
    OPERADORA_CHOICES = [
        ('vivo', 'Vivo'),
        ('claro', 'Claro'),
        ('tim', 'TIM'),
        ('oi', 'Oi'),
        ('outras', 'Outras'),
    ]
    
    numero = models.CharField(max_length=15, unique=True, verbose_name="Número da Linha")
    ACAO_CHOICES = [
        ('TT', 'TT'),
        ('PORTABILIDADE', 'PORTABILIDADE'),
        ('ESTOQUE', 'ESTOQUE'),
    ]
    iccid = models.CharField(max_length=25, verbose_name="ICCID", default="", blank=True, null=True)
    cnpj = models.CharField(max_length=18, verbose_name="CNPJ", default="")
    empresa = models.CharField(max_length=100, verbose_name="Cliente", default="")
    rp = models.CharField(max_length=50, verbose_name="RP", default="")
    tipo_plano = models.CharField(max_length=50, choices=TIPO_CHOICES, verbose_name="Tipo de Plano")
    valor_plano = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor do Plano (R$)")
    taxa_manutencao = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Taxa de Manutenção (R$)", default=0)
    ativa = models.BooleanField(default=True, verbose_name="Linha Ativa")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Criado por")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    def __str__(self):
        return f"{self.numero} - {self.nome_titular}"

    class Meta:
        ordering = ['numero']
        verbose_name = 'Linha de Telefonia'
        verbose_name_plural = 'Linhas de Telefonia'
