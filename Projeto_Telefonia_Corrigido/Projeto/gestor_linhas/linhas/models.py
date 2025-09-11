from django.db import models
from django.contrib.auth.models import User

class Linha(models.Model):
    TIPO_CHOICES = [
        ('pre', 'Pré-pago'),
        ('pos', 'Pós-pago'),
        ('controle', 'Controle'),
    ]
    
    OPERADORA_CHOICES = [
        ('vivo', 'Vivo'),
        ('claro', 'Claro'),
        ('tim', 'TIM'),
        ('oi', 'Oi'),
        ('outras', 'Outras'),
    ]
    
    numero = models.CharField(max_length=15, unique=True, verbose_name="Número da Linha")
    nome_titular = models.CharField(max_length=100, verbose_name="Nome do Titular")
    operadora = models.CharField(max_length=20, choices=OPERADORA_CHOICES, verbose_name="Operadora")
    tipo_plano = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo de Plano")
    valor_plano = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor do Plano (R$)")
    data_contratacao = models.DateField(verbose_name="Data de Contratação")
    data_vencimento = models.IntegerField(choices=[(i, i) for i in range(1, 32)], verbose_name="Dia do Vencimento")
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
