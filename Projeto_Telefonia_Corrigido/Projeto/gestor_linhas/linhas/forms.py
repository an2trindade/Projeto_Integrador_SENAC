from django import forms
from .models import Linha

class LinhaForm(forms.ModelForm):
    class Meta:
        model = Linha
        fields = ['numero', 'nome_titular', 'operadora', 'tipo_plano', 'valor_plano', 
                 'data_contratacao', 'data_vencimento', 'ativa', 'observacoes']
        widgets = {
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999'
            }),
            'nome_titular': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo do titular'
            }),
            'operadora': forms.Select(attrs={
                'class': 'form-select'
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
            'data_contratacao': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'data_vencimento': forms.Select(attrs={
                'class': 'form-select'
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
        
        if len(numero_limpo) < 10 or len(numero_limpo) > 11:
            raise forms.ValidationError('Número deve ter 10 ou 11 dígitos.')
        
        # Verifica se já existe outro registro com o mesmo número
        if Linha.objects.filter(numero=numero).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError('Já existe uma linha com este número.')
        
        return numero

class BuscaLinhaForm(forms.Form):
    busca = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por número, titular ou operadora...'
        })
    )
    operadora = forms.ChoiceField(
        choices=[('', 'Todas as operadoras')] + Linha.OPERADORA_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    tipo_plano = forms.ChoiceField(
        choices=[('', 'Todos os tipos')] + Linha.TIPO_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    ativa = forms.ChoiceField(
        choices=[('', 'Todas'), ('True', 'Ativas'), ('False', 'Inativas')],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

