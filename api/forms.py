from django import forms
from .models import Cliente, Cotacao, Motorista, Financeiro, Agregado

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nome_razaosocial', 'tipo', 'cpf_cnpj', 'telefone_1', 'telefone_2',
            'email', 'cidade', 'uf', 'cep', 'rua', 'bairro', 'numero'
        ]
        widgets = {
            'nome_razaosocial': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'cpf_cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone_1': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone_2': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_cep'}),
            'rua': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_rua'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_bairro'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_cidade'}),
            'uf': forms.Select(attrs={'class': 'form-control', 'id': 'id_uf'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'nome_razaosocial':'Nome / Razão Social',
            'cpf_cnpj': 'CPF / CNPJ'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'telefone_2':
                field.required = True



#---------------------------------------------------------------------------------------------------------------------------

class ColetaForm(forms.ModelForm):
    class Meta:
        model = Cotacao
        fields = [
            'cliente',
            
            'cep_origem', 'rua_origem', 'numero_origem', 'bairro_origem', 'cidade_origem', 'uf_origem',

            'cep_destino', 'rua_destino', 'numero_destino', 'bairro_destino', 'cidade_destino', 'uf_destino',

            'peso', 'dimensoes', 'valor_carga', 'data_coleta', 'tipo_frete', 'descricao_produto'
        ]
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'cep_origem': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP de Origem', 'id': 'cepOrigem'}),
            'rua_origem': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'id': 'ruaOrigem'}),
            'numero_origem': forms.TextInput(attrs={'class': 'form-control', 'id': 'numeroOrigem'}),
            'bairro_origem': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'id': 'bairroOrigem'}),
            'cidade_origem': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'id': 'cidadeOrigem'}),
            'uf_origem': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'id': 'ufOrigem'}),

            'cep_destino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP de Destino', 'id': 'cepDestino'}),
            'rua_destino': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'id': 'ruaDestino'}),
            'numero_destino': forms.TextInput(attrs={'class': 'form-control', 'id': 'numeroDestino'}),
            'bairro_destino': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'id': 'bairroDestino'}),
            'cidade_destino': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'id': 'cidadeDestino'}),
            'uf_destino': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'id': 'ufDestino'}),

            'peso': forms.NumberInput(attrs={'class': 'form-control'}),
            'dimensoes': forms.TextInput(attrs={'class': 'form-control'}),
            'valor_carga': forms.NumberInput(attrs={'class': 'form-control'}),
            'data_coleta': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tipo_frete': forms.Select(attrs={'class': 'form-control'}),
            'descricao_produto': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
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
            'nome','tipo','cpf_cnpj','celular','telefone','tipo_de_veiculo','placa','email','cidade_base','disponibilidade',
        ]
        
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Motorista'}),
            'tipo': forms.HiddenInput(attrs={'value': 'PR'}),
            'cpf_cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF/CNPJ'}),
            'celular': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Celular'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}),
            'tipo_de_veiculo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo de Veículo'}),
            'placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Placa'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'cidade_base': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade Base'}),
            'disponibilidade': forms.Select(attrs={'class': 'form-control'}),
        }
        
        labels = {
            'nome': 'Nome',
            'tipo': 'Tipo de Motorista',
            'cpf_cnpj': 'CPF/CNPJ',
            'celular': 'Celular/Whatsapp',
            'telefone': 'Telefone',
            'tipo_de_veiculo': 'Tipo de Veículo',
            'placa': 'Placa do Veículo',
            'email': 'Email',
            'cidade_base': 'Cidade Base',
            'disponibilidade': 'Disponibilidade',
    }
#--------------------------------------------------------------AGREGADO----------------------------------------------------
class AgregadoForm(forms.ModelForm):
    class Meta:
        model = Agregado
        fields = [
            # Dados Pessoais
            'nome_completo', 'cpf', 'rg', 'orgao_emissor', 'data_emissao_rg',
            'cnh', 'data_nascimento',

            # Contato
            'telefone', 'celular', 'celular2', 'email',
            'cep', 'rua', 'numero', 'bairro', 'cidade', 'estado',

            # Veículo
            'tipo_veiculo', 'marca_modelo', 'ano_fabricacao',
            'placa', 'cor', 'capacidade_carga',

            # Financeiro
            'banco', 'agencia', 'conta', 'tipo_conta', 'pix',

            # Outros
            'cidade_base', 'disponibilidade', 'ultima_roteirizacao'
        ]

        widgets = {
            # Dados Pessoais
            'nome_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'rg': forms.TextInput(attrs={'class': 'form-control'}),
            'orgao_emissor': forms.TextInput(attrs={'class': 'form-control'}),
            'data_emissao_rg': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cnh': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            

            # Contato
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'celular2': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_cep'}),
            'rua': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_rua'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_bairro'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_cidade'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_uf'}),


            # Veículo
            'tipo_veiculo': forms.TextInput(attrs={'class': 'form-control'}),
            'marca_modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'ano_fabricacao': forms.NumberInput(attrs={'class': 'form-control'}),
            'placa': forms.TextInput(attrs={'class': 'form-control'}),
            'cor': forms.TextInput(attrs={'class': 'form-control'}),
            'capacidade_carga': forms.TextInput(attrs={'class': 'form-control'}),

            # Financeiro
            'banco': forms.TextInput(attrs={'class': 'form-control'}),
            'agencia': forms.TextInput(attrs={'class': 'form-control'}),
            'conta': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_conta': forms.Select(attrs={'class': 'form-control'}),
            'pix': forms.TextInput(attrs={'class': 'form-control'}),

            # Outros
            'cidade_base': forms.TextInput(attrs={'class': 'form-control'}),
            'disponibilidade': forms.Select(attrs={'class': 'form-control'}),
            'ultima_roteirizacao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

        labels = {
            'nome_completo': 'Nome Completo / Razão Social',
            'cpf': 'CPF / CNPJ',
            'rg': 'RG',
            'orgao_emissor': 'Órgão Emissor',
            'data_emissao_rg': 'Data de Emissão do RG',
            'cnh': 'CNH',
            'data_nascimento': 'Data de Nascimento',
            'telefone': 'Telefone Fixo',
            'celular': 'Celular (WhatsApp)',
            'celular2': 'Celular 2 (Opcional)',
            'email': 'E-mail',
            'cep': 'CEP',
            'rua': 'Rua',
            'numero': 'Número',
            'bairro': 'Bairro',
            'cidade': 'Cidade',
            'estado': 'Estado',
            'tipo_veiculo': 'Tipo de Veículo',
            'marca_modelo': 'Marca/Modelo',
            'ano_fabricacao': 'Ano de Fabricação',
            'placa': 'Placa',
            'cor': 'Cor',
            'capacidade_carga': 'Capacidade de Carga',
            'banco': 'Banco',
            'agencia': 'Agência',
            'conta': 'Conta',
            'tipo_conta': 'Tipo de Conta',
            'pix': 'Chave PIX',
            'cidade_base': 'Cidade Base',
            'disponibilidade': 'Disponibilidade',
            'ultima_roteirizacao': 'Última Roteirização',
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
