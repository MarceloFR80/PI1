from django import forms
from .models import Cliente, Cotacao

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nome_razaosocial', 'tipo', 'cpf_cnpj', 'telefone_1', 'telefone_2',
            'email', 'cidade', 'uf', 'cep', 'rua', 'bairro', 'numero'
        ]
        widgets = {
            'nome_razaosocial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome/Razão Social'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'cpf_cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF/CNPJ'}),
            'telefone_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone 1'}),
            'telefone_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone 2'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'uf': forms.Select(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP'}),
            'rua': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rua'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'}),
            'numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número'}),
        }

class ColetaForm(forms.ModelForm):
    cpf_cnpj_cliente = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF/CNPJ do Cliente'})
    )

    class Meta:
        model = Cotacao  # ou Coleta
        fields = [
            'cep_origem', 'cep_destino', 'peso', 'dimensoes', 
            'valor_carga', 'data_coleta', 'descricao_produto', 
            'valor_frete', 'cpf_cnpj_cliente'  # Inclui o campo cpf_cnpj_cliente
        ]
        widgets = {
            'cep_origem': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP de Origem'}),
            'cep_destino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP de Destino'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Peso'}),
            'dimensoes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dimensões'}),
            'valor_carga': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Valor da Carga'}),
            'data_coleta': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descricao_produto': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Descrição do Produto'}),
            'valor_frete': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Valor do Frete'}),
        }
