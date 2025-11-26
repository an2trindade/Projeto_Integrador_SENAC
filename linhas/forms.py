from django import forms
from .models import Linha, Cliente, Fidelidade
import re

def validar_cpf(cpf_raw: str) -> bool:
    cpf = re.sub(r'\D', '', cpf_raw or '')
    if not cpf or len(cpf) != 11:
        return False
    if cpf == cpf[0] * 11:
        return False
    def calc(digs):
        s = 0
        for i, d in enumerate(digs):
            s += int(d) * (len(digs) + 1 - i)
        r = s % 11
        return '0' if r < 2 else str(11 - r)
    ver1 = calc(cpf[:9])
    ver2 = calc(cpf[:10])
    return cpf[9] == ver1 and cpf[10] == ver2

def validar_cnpj(cnpj_raw: str) -> bool:
    cnpj = re.sub(r'\D', '', cnpj_raw or '')
    if not cnpj or len(cnpj) != 14:
        return False
    if cnpj == cnpj[0] * 14:
        return False
    def calc(digs, pesos):
        s = 0
        for d, p in zip(digs, pesos):
            s += int(d) * p
        r = s % 11
        return '0' if r < 2 else str(11 - r)
    pesos1 = [5,4,3,2,9,8,7,6,5,4,3,2]
    pesos2 = [6] + pesos1
    ver1 = calc(cnpj[:12], pesos1)
    ver2 = calc(cnpj[:13], pesos2)
    return cnpj[12] == ver1 and cnpj[13] == ver2

class LinhaForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    def clean(self):
        cleaned_data = super().clean()
        tipo_plano = cleaned_data.get('tipo_plano')
        valores_plano = {
            'BLACK_VOZ_GW_800SMS': 14.00,
            'BLACK_1GB_GW_800SMS': 15.90,
            'BLACK_5GB_GW_800SMS': 25.90,
            'BLACK_10GB_GW_800SMS': 29.90,
            'BLACK_20GB_GW_800SMS': 39.90,
            'BLACK_50GB_GW_800SMS': 69.90,
            'BLACK_ILIMITADO_GB_GW_800SMS': 164.00,
        }
        from decimal import Decimal, InvalidOperation
        if tipo_plano in valores_plano:
            # Garante que o valor seja Decimal com 2 casas
            cleaned_data['valor_plano'] = Decimal(str(valores_plano[tipo_plano])).quantize(Decimal('0.01'))

        # Validação de casas decimais
        taxa_manutencao = cleaned_data.get('taxa_manutencao')
        valor_plano = cleaned_data.get('valor_plano')
        if taxa_manutencao is not None:
            try:
                dec = Decimal(str(taxa_manutencao))
                if dec.as_tuple().exponent < -2:
                    self.add_error('taxa_manutencao', 'A taxa de manutenção deve ter no máximo 2 casas decimais.')
            except InvalidOperation:
                self.add_error('taxa_manutencao', 'Valor inválido para taxa de manutenção.')
        if valor_plano is not None:
            try:
                dec = Decimal(str(valor_plano))
                if dec.as_tuple().exponent < -2:
                    self.add_error('valor_plano', 'O valor do plano deve ter no máximo 2 casas decimais.')
            except InvalidOperation:
                self.add_error('valor_plano', 'Valor inválido para valor do plano.')
        return cleaned_data
    class Meta:
        model = Linha
        fields = [
            # CLIENTE
            'cliente', 'empresa', 'cnpj', 'taxa_manutencao', 'rp',
            # LINHA
            'numero', 'tipo_plano', 'valor_plano',
            # AÇÃO
            'acao', 'observacoes',
            # campos extras
            'iccid', 'ativa'
        ]
        widgets = {
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999'
            }),
            'iccid': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ICCID do chip',
                'required': False
            }),
            'acao': forms.Select(attrs={
                'class': 'form-select'
            }),
            'cnpj': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'CNPJ do cliente',
                'maxlength': '18',
                'inputmode': 'numeric',
                'autocomplete': 'off'
            }),
            'empresa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do cliente'
            }),
            'rp': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'RP'
            }),
            'tipo_plano': forms.Select(attrs={
                'class': 'form-select'
            }),
            'valor_plano': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'taxa_manutencao': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'ativa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações adicionais (opcional)'
            })
        }

    def clean_numero(self):
        numero = self.cleaned_data['numero']
        # Remove caracteres não numéricos
        numero_limpo = ''.join(filter(str.isdigit, numero))
        if len(numero_limpo) != 11:
            raise forms.ValidationError('O número da linha deve conter exatamente 11 dígitos.')
        # Verifica se já existe outro registro com o mesmo número
        if Linha.objects.filter(numero=numero).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError('Já existe uma linha com este número.')
        return numero

class BuscaLinhaForm(forms.Form):
    busca = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control custom-busca',
            'placeholder': '🔎 Buscar por CNPJ, nome do cliente, número da linha ou RP...',
            'style': 'width: 400px; max-width: 100%; border-radius: 25px; border: 2px solid #00796b; transition: box-shadow 0.3s;',
        })
    )
    # Campo de operadora removido
    tipo_plano = forms.ChoiceField(
        choices=[('', 'Todos os tipos')] + Linha.TIPO_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    ativa = forms.ChoiceField(
        choices=[
            ('', 'Todas'),
            ('ativa', 'Ativa'),
            ('cancelada', 'Cancelada'),
            ('transferida', 'Transferida'),
            ('suspensa', 'Suspensa'),
            ('inativa', 'Inativa'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )


# Formulário base (mantido para compatibilidade)
class ClienteForm(forms.ModelForm):
    """Formulário de Cliente com requisitos condicionais para PF/PJ.

    Regras:
    - Campo tipo_pessoa controla validação.
    - Para PF: cnpj, razao_social, fantasia não são obrigatórios.
    - Para PJ: cnpj e razao_social obrigatórios; fantasia opcional.
    - Campos comuns (empresa, nome_dono, cpf_dono, data_nascimento_dono, endereco_completo, contato) sempre obrigatórios.
    - email é opcional (mas validado se presente).
    """

    tipo_pessoa = forms.ChoiceField(
        choices=Cliente.TIPO_PESSOA_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )
    # Aceita DD/MM/YYYY ou YYYY-MM-DD (caso vindo de input type=date)
    data_nascimento_dono = forms.DateField(
        required=True,
        input_formats=['%d/%m/%Y', '%Y-%m-%d'],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'DD/MM/AAAA'
        })
    )

    class Meta:
        model = Cliente
        fields = ['tipo_pessoa', 'empresa', 'cnpj', 'razao_social', 'fantasia', 'endereco_completo', 'contato', 'email', 'telefone', 'nome_dono', 'cpf_dono', 'data_nascimento_dono']
        widgets = {
            'empresa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome / Razão social'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00.000.000/0000-00'}),
            'razao_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Razão social'}),
            'fantasia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome fantasia'}),
            'endereco_completo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Logradouro, número, complemento, bairro, cidade - UF'}),
            'contato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone de contato (somente número)', 'inputmode': 'tel', 'maxlength': '15'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(11) 99999-9999', 'inputmode': 'tel'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'contato@exemplo.com'}),
            'nome_dono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do proprietário'}),
            'cpf_dono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tipo = (self.data.get('tipo_pessoa') if self.data else None) or self.initial.get('tipo_pessoa') or 'PJ'
        self.fields['tipo_pessoa'].initial = tipo
        # Definir obrigatoriedade condicional
        is_pf = (tipo == 'PF')
        # Campos sempre obrigatórios
        for nome in ['empresa', 'nome_dono', 'cpf_dono', 'data_nascimento_dono', 'endereco_completo', 'contato']:
            self.fields[nome].required = True
        # Email opcional
        self.fields['email'].required = False
        self.fields['telefone'].required = False
        # Campos PJ condicionais
        self.fields['cnpj'].required = not is_pf
        self.fields['razao_social'].required = not is_pf
        self.fields['fantasia'].required = False  # opcional para ambos

    def clean_cpf_dono(self):
        cpf = self.cleaned_data.get('cpf_dono', '').strip()
        digits = re.sub(r'\D', '', cpf)
        if not digits:
            raise forms.ValidationError('CPF obrigatório.')
        if not validar_cpf(digits):
            raise forms.ValidationError('CPF inválido.')
        return cpf

    def clean_cnpj(self):
        tipo = self.cleaned_data.get('tipo_pessoa') or self.fields['tipo_pessoa'].initial
        cnpj = self.cleaned_data.get('cnpj', '').strip()
        digits = re.sub(r'\D', '', cnpj)
        if tipo == 'PF':
            # Não obrigatório para PF; se vazio retorna vazio sem erro
            if not digits:
                return ''
            # Se preenchido, validar
            if not validar_cnpj(digits):
                raise forms.ValidationError('CNPJ inválido.')
            return cnpj
        # PJ obrigatório
        if not digits:
            raise forms.ValidationError('CNPJ obrigatório.')
        if not validar_cnpj(digits):
            raise forms.ValidationError('CNPJ inválido.')
        return cnpj

    def clean_razao_social(self):
        tipo = self.cleaned_data.get('tipo_pessoa') or self.fields['tipo_pessoa'].initial
        valor = self.cleaned_data.get('razao_social', '').strip()
        if tipo == 'PF':
            return ''  # ignora para PF
        if not valor:
            raise forms.ValidationError('Razão social obrigatória para PJ.')
        return valor

    def clean_contato(self):
        contato = self.cleaned_data.get('contato', '').strip()
        digits = re.sub(r'\D', '', contato)
        if not digits:
            raise forms.ValidationError('Telefone de contato obrigatório.')
        if len(digits) not in (10, 11):
            raise forms.ValidationError('Telefone inválido: use 10 ou 11 dígitos.')
        return contato

    def clean(self):
        cleaned = super().clean()
        tipo = cleaned.get('tipo_pessoa') or self.fields['tipo_pessoa'].initial
        # Para PF: garantir que empresa reflita nome do titular se vazio
        if tipo == 'PF':
            empresa = cleaned.get('empresa', '').strip()
            nome = cleaned.get('nome_dono', '').strip()
            if not empresa and nome:
                cleaned['empresa'] = nome
        return cleaned


class FidelidadeForm(forms.ModelForm):
    """
    Formulário para cadastro de fidelidade de linhas
    """
    numero_linha = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o número da linha',
            'autocomplete': 'off'
        }),
        label='Número da Linha'
    )
    
    class Meta:
        model = Fidelidade
        fields = ['observacoes']
        widgets = {
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Digite aqui as observações sobre a fidelidade desta linha...',
                'required': True
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['observacoes'].required = True
    
    def clean_numero_linha(self):
        numero = self.cleaned_data['numero_linha'].strip()
        
        if not numero:
            raise forms.ValidationError('Número da linha é obrigatório.')
        
        # Verificar se a linha existe
        try:
            linha = Linha.objects.get(numero=numero)
            self.cleaned_data['linha'] = linha
            return numero
        except Linha.DoesNotExist:
            raise forms.ValidationError('Linha não encontrada. Verifique o número informado.')
    
    def clean_observacoes(self):
        observacoes = self.cleaned_data.get('observacoes', '').strip()
        
        if not observacoes:
            raise forms.ValidationError('Observações são obrigatórias.')
        
        if len(observacoes) < 10:
            raise forms.ValidationError('Observações devem ter pelo menos 10 caracteres.')
        
        return observacoes
    
    def save(self, commit=True, user=None):
        fidelidade = super().save(commit=False)
        fidelidade.linha = self.cleaned_data['linha']
        
        if user:
            fidelidade.criado_por = user
        
        if commit:
            fidelidade.save()
        
        return fidelidade

