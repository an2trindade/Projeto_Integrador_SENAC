from django import forms
from .models import Linha, Cliente
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
                'placeholder': 'CNPJ do cliente'
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


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['empresa', 'cnpj', 'razao_social', 'fantasia', 'endereco_completo', 'contato', 'telefone', 'nome_dono', 'cpf_dono', 'data_nascimento_dono']
        widgets = {
            'empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'razao_social': forms.TextInput(attrs={'class': 'form-control'}),
            'fantasia': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco_completo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contato': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_dono': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf_dono': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento_dono': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean_cpf_dono(self):
        cpf = self.cleaned_data.get('cpf_dono', '').strip()
        digits = re.sub(r'\D', '', cpf)
        if digits:
            if not validar_cpf(digits):
                raise forms.ValidationError('CPF inválido: verifique o número informado.')
        return cpf

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj', '').strip()
        digits = re.sub(r'\D', '', cnpj)
        if digits:
            if not validar_cnpj(digits):
                raise forms.ValidationError('CNPJ inválido: verifique o número informado.')
        return cnpj

