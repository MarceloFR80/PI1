from django import forms
from .models import Cliente, Cotacao, Motorista, Financeiro

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

            # Estes precisam ter ID específico para o JS funcionar:
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP', 'id': 'id_cep'}),
            'rua': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rua', 'id': 'id_rua'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro', 'id': 'id_bairro'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade', 'id': 'id_cidade'}),
            'uf': forms.Select(attrs={'class': 'form-control', 'id': 'id_uf'}),

            'numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número'}),
        }


#---------------------------------------------------------------------------------------------------------------------------

class ColetaForm(forms.ModelForm):
    class Meta:
        model = Cotacao
        fields = [
            'cliente', 'cep_origem', 'cep_destino', 'peso', 'dimensoes',
            'valor_carga', 'data_coleta', 'tipo_frete', 'descricao_produto'
        ]
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'cep_origem': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP de Origem'}),
            'cep_destino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP de Destino'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Peso'}),
            'dimensoes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dimensões (m³)'}),
            'valor_carga': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Valor da Carga'}),
            'data_coleta': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tipo_frete': forms.Select(attrs={'class': 'form-control'}),
            'descricao_produto': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Descrição do Produto'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Cliente.objects.all()
        self.fields['cliente'].label = "Cliente (Nome/Razão Social - CPF/CNPJ)"
        self.fields['cliente'].empty_label = "Selecione um cliente"
        self.fields['cliente'].label_from_instance = lambda obj: f"{obj.nome_razaosocial} - {obj.cpf_cnpj}"

#-------------------------------------------------------------------------------------------------------------------------------------------
class MotoristaForm(forms.ModelForm):
    class Meta:
        model = Motorista
        fields = [
            'nome', 
            'tipo', 
            'cpf_cnpj', 
            'celular', 
            'telefone', 
            'tipo_de_veiculo', 
            'placa', 
            'email'
        ]
        
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Motorista'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'cpf_cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF/CNPJ'}),
            'celular': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Celular'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}),
            'tipo_de_veiculo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo de Veículo'}),
            'placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Placa'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
        
        labels = {
            'nome': 'Nome',
            'tipo': 'Tipo de Motorista',
            'cpf_cnpj': 'CPF/CNPJ',
            'celular': 'Celular',
            'telefone': 'Telefone',
            'tipo_de_veiculo': 'Tipo de Veículo',
            'placa': 'Placa do Veículo',
            'email': 'Email',
        }

#------------------------------------------------FINANCEIRO----------------------------------------------
class FinanceiroForm(forms.ModelForm):
    class Meta:
        model = Financeiro
        fields = ['descricao', 'valor', 'data_operacao', 'operacao']
        
    data_operacao = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Data de Operação"
    )
