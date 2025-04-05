from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum

class Cliente(models.Model):
    TIPO_CHOICES = (
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    )

    ESTADOS_CHOICES = (
        ('--', 'Selecione um estado'),('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
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
    rua = models.CharField(max_length=100, default="--")
    bairro = models.CharField(max_length=100, default="------")
    numero = models.CharField(max_length=10, default="S/N")

    def __str__(self):
     return f"{self.nome_razaosocial} - {self.cpf_cnpj}"
    #{self.nome_razaosocial} - 
#----------------------------------------------------------------------------------------------------------------------------------------
class Cotacao(models.Model):
    TIPOFRETE_CHOICES = (
        ('NO', 'Frete Normal'),
        ('EX', 'Frete Expresso'),
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='cotações')
    cep_origem = models.CharField(max_length=9)
    rua_origem = models.CharField(max_length=100, blank=True, null=True)
    numero_origem = models.CharField(max_length=10, blank=True, null=True)
    bairro_origem = models.CharField(max_length=100, blank=True, null=True)
    cidade_origem = models.CharField(max_length=100, blank=True, null=True)
    uf_origem = models.CharField(max_length=2, blank=True, null=True)

    cep_destino = models.CharField(max_length=9)
    rua_destino = models.CharField(max_length=100, blank=True, null=True)
    numero_destino = models.CharField(max_length=10, blank=True, null=True)
    bairro_destino = models.CharField(max_length=100, blank=True, null=True)
    cidade_destino = models.CharField(max_length=100, blank=True, null=True)
    uf_destino = models.CharField(max_length=2, blank=True, null=True)

    peso = models.DecimalField(max_digits=8, decimal_places=2)
    dimensoes = models.CharField(max_length=20)
    valor_carga = models.DecimalField(max_digits=10, decimal_places=2)
    data_coleta = models.DateField()
    tipo_frete = models.CharField(max_length=20, choices=TIPOFRETE_CHOICES, default="NO")
    descricao_produto = models.TextField()
    valor_frete = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.cliente:
            raise ValidationError("Cliente não selecionado.")

    def __str__(self):
        return f"Cotação de {self.cep_origem} para {self.cep_destino}"


#-----------------------------------------------------------------MOTORISTAS-------------------------------------------------------
class Motorista(models.Model):
    TIPO_CHOICES = (
        ('PR', 'Motorista Próprio'),
        ('AG', 'Motorista Agregado'),
    )
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES)
    cpf_cnpj = models.CharField(max_length=18, unique=True)
    celular = models.CharField(max_length=15, default='')          # Novo campo celular
    telefone = models.CharField(max_length=15)
    tipo_de_veiculo = models.CharField(max_length=50, default='')
    placa = models.CharField(max_length=8, default='')
    email = models.EmailField()
    
    
    def __str__(self):
        return self.nome
#-----------------------------------------------------------------FINANCEIRO-----------------------------------------------------------
class Financeiro(models.Model):
    OPERACAO_CHOICES = [
        ('CR', 'Crédito'),
        ('DB', 'Débito'),
    ]

    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_operacao = models.DateField()
    operacao = models.CharField(max_length=2, choices=OPERACAO_CHOICES)

    def __str__(self):
        return self.descricao

    @property
    def receitas(self):
        # Calcula a receita total de todas as operações de crédito
        return Financeiro.objects.filter(operacao='CR').aggregate(total=Sum('valor'))['total'] or 0

    @property
    def despesas(self):
        # Calcula a despesa total de todas as operações de débito
        return Financeiro.objects.filter(operacao='DB').aggregate(total=Sum('valor'))['total'] or 0

    @property
    def lucro_prejuizo(self):
        # Calcula o lucro/prejuízo com base na receita e despesa totais
        return self.receitas - self.despesas