from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class LoginAttempt(models.Model):
    username = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    attempt_time = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)
    blocked_until = models.DateTimeField(null=True, blank=True)
    attempt_count = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.username} - {self.ip_address} - Tentativas: {self.attempt_count}"

    class Meta:
        ordering = ['-attempt_time']

    def is_currently_blocked(self):
        if not self.is_blocked:
            return False
        return timezone.now() < self.blocked_until

class Cliente(models.Model):
    empresa = models.CharField(max_length=150, verbose_name='Empresa')
    cnpj = models.CharField(max_length=18, verbose_name='CNPJ', blank=True, default='')
    razao_social = models.CharField(max_length=200, verbose_name='Razão Social', blank=True, default='')
    fantasia = models.CharField(max_length=200, verbose_name='Nome Fantasia', blank=True, default='')
    endereco_completo = models.TextField(verbose_name='Endereço completo', blank=True, default='')
    contato = models.CharField(max_length=100, verbose_name='Contato', blank=True, default='')
    telefone = models.CharField(max_length=30, verbose_name='Telefone', blank=True, default='')
    email = models.EmailField(max_length=254, verbose_name='Email', blank=True, default='')
    nome_dono = models.CharField(max_length=150, verbose_name='Nome do Titular / Dono', blank=True, default='')
    cpf_dono = models.CharField(max_length=20, verbose_name='CPF do Dono', blank=True, default='')
    data_nascimento_dono = models.DateField(verbose_name='Data de Nascimento do Dono', null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['empresa']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f"{self.empresa} ({self.cnpj})" if self.cnpj else self.empresa

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
    # Campo 'acao' foi removido/alterado em migrações anteriores; reintroduzimos aqui
    # para manter o modelo consistente com as views/templates que dependem dele.
    acao = models.CharField(max_length=20, choices=ACAO_CHOICES, default='TT', verbose_name='Ação')
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
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Cliente vinculado')
    # restore representation and meta for Linha
    def __str__(self):
        # fallback if nome_titular does not exist on all records
        nome = getattr(self, 'nome_titular', '')
        return f"{self.numero} - {nome}" if nome else f"{self.numero}"

    class Meta:
        ordering = ['numero']
        verbose_name = 'Linha de Telefonia'
        verbose_name_plural = 'Linhas de Telefonia'


class Protocolo(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_andamento', 'Em andamento'),
        ('resolvido', 'Resolvido'),
        ('cancelado', 'Cancelado'),
    ]

    titulo = models.CharField(max_length=200, verbose_name='Título')
    descricao = models.TextField(blank=True, null=True, verbose_name='Descrição')
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Criado por')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente', verbose_name='Status')

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Protocolo'
        verbose_name_plural = 'Protocolos'

    def __str__(self):
        return f"{self.titulo} ({self.get_status_display()})"


class Fidelidade(models.Model):
    """
    Modelo para registrar informações de fidelidade das linhas
    """
    linha = models.ForeignKey(Linha, on_delete=models.CASCADE, verbose_name='Linha', related_name='fidelidades')
    observacoes = models.TextField(verbose_name='Observações', help_text='Observações sobre a fidelidade da linha')
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Criado por')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Fidelidade'
        verbose_name_plural = 'Fidelidades'
    
    def __str__(self):
        return f"Fidelidade - Linha {self.linha.numero} ({self.criado_em.strftime('%d/%m/%Y')})"


class UsuarioEmpresa(models.Model):
    """
    Modelo para armazenar dados empresariais dos usuários do sistema
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário', related_name='usuario_empresa')
    cnpj = models.CharField(max_length=18, verbose_name='CNPJ')
    razao_social = models.CharField(max_length=200, verbose_name='Razão Social')
    nome_fantasia = models.CharField(max_length=200, verbose_name='Nome Fantasia', blank=True, default='')
    endereco = models.CharField(max_length=500, verbose_name='Endereço')
    telefone = models.CharField(max_length=15, verbose_name='Telefone')
    nome_completo_agente = models.CharField(max_length=200, verbose_name='Nome Completo do Agente', blank=True, default='')
    cpf_agente = models.CharField(max_length=14, verbose_name='CPF do Agente')
    data_nascimento_agente = models.DateField(verbose_name='Data de Nascimento do Agente')
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Criado por', related_name='usuarios_empresas_criados')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        ordering = ['razao_social']
        verbose_name = 'Usuário Empresa'
        verbose_name_plural = 'Usuários Empresas'
    
    def __str__(self):
        return f"{self.razao_social} ({self.user.username})"
