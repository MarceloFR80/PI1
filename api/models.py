from django.db import models
from django.core.exceptions import ValidationError

class Cliente(models.Model):
    TIPO_CHOICES = (
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    )

    ESTADOS_CHOICES = (
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
    )

    nome_razaosocial = models.CharField(max_length=100, default="------")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default="PF")
    cpf_cnpj = models.CharField(max_length=20, unique=True, default="000.000.000-00")
    telefone_1 = models.CharField(max_length=20, default="(00) 0000-0000")
    telefone_2 = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True, default="email@exemplo.com")

    cidade = models.CharField(max_length=100, default="------")
    uf = models.CharField(max_length=2, choices=ESTADOS_CHOICES, default="--")
    cep = models.CharField(max_length=10, default="00000-000")
    rua = models.CharField(max_length=100, default="------")
    bairro = models.CharField(max_length=100, default="------")
    numero = models.CharField(max_length=10, default="S/N")

    def __str__(self):
        return self.nome_razaosocial


class Cotacao(models.Model):
    cep_origem = models.CharField(max_length=9)
    cep_destino = models.CharField(max_length=9)
    peso = models.DecimalField(max_digits=8, decimal_places=2)
    dimensoes = models.CharField(max_length=20)
    valor_carga = models.DecimalField(max_digits=10, decimal_places=2)
    data_coleta = models.DateField()
    descricao_produto = models.TextField()
    valor_frete = models.DecimalField(max_digits=10, decimal_places=2)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    # Relacionamento indireto via CPF/CNPJ
    cpf_cnpj_cliente = models.CharField(max_length=20)  # Adiciona este campo

    def __str__(self):
        return f"Cotação de {self.cep_origem} para {self.cep_destino}"

    def clean(self):
        # Verifica se existe um cliente com o CPF/CNPJ fornecido
        if not Cliente.objects.filter(cpf_cnpj=self.cpf_cnpj_cliente).exists():
            raise ValidationError(f"Cliente com CPF/CNPJ {self.cpf_cnpj_cliente} não encontrado.")

    @property
    def cliente(self):
        # Obtém o cliente associado ao CPF/CNPJ, se existir
        return Cliente.objects.filter(cpf_cnpj=self.cpf_cnpj_cliente).first()
