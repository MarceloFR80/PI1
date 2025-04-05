from rest_framework import serializers
from .models import Cliente
from .models import Cotacao  # Supondo que você tenha um modelo Cotacao

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            'id',  # Certifique-se de incluir o campo 'id' para que ele apareça na resposta da API
            'nome_razaosocial', 'tipo', 'cpf_cnpj', 'telefone_1', 'telefone_2',
            'email', 'cidade', 'uf', 'cep', 'rua', 'bairro', 'numero'
        ]
#-------------------------------------COTAÇÃO-------------------------------------------------------

class CotacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cotacao
        fields = [
            'cliente',

            'cep_origem', 'rua_origem', 'numero_origem', 'bairro_origem',
            'cidade_origem', 'uf_origem',

            'cep_destino', 'rua_destino', 'numero_destino', 'bairro_destino',
            'cidade_destino', 'uf_destino',

            'peso', 'dimensoes', 'valor_carga', 'data_coleta',
            'tipo_frete', 'descricao_produto', 'valor_frete'
        ]
