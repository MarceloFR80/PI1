from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum

class Cliente(models.Model):
    TIPO_CHOICES = (
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    )

    ESTADOS_CHOICES = (
        ('--', 'Selecione um estado'), ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
    )

    nome_razaosocial = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    cpf_cnpj = models.CharField(max_length=20, unique=True)
    telefone_1 = models.CharField(max_length=20)
    telefone_2 = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)

    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2, choices=ESTADOS_CHOICES)
    cep = models.CharField(max_length=10)
    rua = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nome_razaosocial} - {self.cpf_cnpj}"

#----------------------------------------------------------------------------------------------------------------------------------------
class Cotacao(models.Model):
    TIPOFRETE_CHOICES = (
        ('NO', 'Frete Normal'),
        ('EX', 'Frete Expresso'),
    )

    STATUS_COLETA_CHOICES = (
        ('PENDENTE', 'Pendente'),
        ('REALIZADA', 'Realizada'),
        ('NAO_REALIZADA', 'Não Realizada'),
    )

    STATUS_ENTREGA_CHOICES = (
        ('PENDENTE', 'Pendente'),
        ('ENTREGUE', 'Entregue'),
        ('NAO_ENTREGUE', 'Não Entregue'),
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

    status_coleta = models.CharField(max_length=20, choices=STATUS_COLETA_CHOICES, default='PENDENTE')
    status_entrega = models.CharField(max_length=20, choices=STATUS_ENTREGA_CHOICES, default='PENDENTE')
    veiculo = models.CharField(max_length=50, blank=True, null=True)


    def clean(self):
        if not self.cliente:
            raise ValidationError("Cliente não selecionado.")

    def __str__(self):
        return f"Cotação de {self.cep_origem} para {self.cep_destino}"

#-----------------------------------------------------------------MOTORISTAS-------------------------------------------------------
class Motorista(models.Model):
    TIPO_CHOICES = (
        ('PR', 'Próprio'),
        ('AG', 'Agregado'),
    )

    DISPONIBILIDADE_CHOICES = (
        ('DISPONIVEL', 'Disponível'),
        ('INDISPONIVEL', 'Indisponível'),
    )

    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES, default='PR')
    cpf_cnpj = models.CharField(max_length=18, unique=True)
    celular = models.CharField(max_length=15, default='')
    telefone = models.CharField(max_length=15)
    tipo_de_veiculo = models.CharField(max_length=50, default='')
    placa = models.CharField(max_length=8, default='')
    email = models.EmailField()

    disponibilidade = models.CharField(max_length=15, choices=DISPONIBILIDADE_CHOICES, default='DISPONIVEL')
    ultima_roteirizacao = models.DateField(null=True, blank=True)
    cidade_base = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
        return f"{self.nome} ({self.placa})"
#-----------------------------------------------------------------AGREGADO------------------------------------------------------------
class Agregado(models.Model):
    TIPO_CHOICES = (('PR', 'Próprio'), ('AG', 'Agregado'),)
    DISPONIBILIDADE_CHOICES = [('DISPONIVEL', 'Disponível'), ('INDISPONIVEL', 'Indisponível')]
    TIPO_CONTA_CHOICES = [('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')]

    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES, default='AG')

    # Dados Pessoais
    nome_completo = models.CharField("Nome Completo", max_length=255)
    cpf = models.CharField("CPF", max_length=14, unique=True)
    rg = models.CharField("RG", max_length=20)
    orgao_emissor = models.CharField("Órgão Emissor", max_length=20)
    data_emissao_rg = models.DateField("Data de Emissão do RG")
    cnh = models.CharField("CNH", max_length=20)
    data_nascimento = models.DateField("Data de Nascimento")
    

    # Contato
    telefone = models.CharField("Telefone Fixo", max_length=15, blank=True, null=True)
    celular = models.CharField("Celular (WhatsApp)", max_length=15)
    celular2 = models.CharField("Celular 2 (Opcional)", max_length=15, blank=True, null=True)
    email = models.EmailField("E-mail", blank=True, null=True)

    # Endereço
    cep = models.CharField("CEP", max_length=9)
    rua = models.CharField("Rua", max_length=100)
    numero = models.CharField("Número", max_length=10)
    bairro = models.CharField("Bairro", max_length=100)
    cidade = models.CharField("Cidade", max_length=100)
    estado = models.CharField("Estado", max_length=2)

    # Veículo
    tipo_veiculo = models.CharField("Tipo de Veículo", max_length=50)
    marca_modelo = models.CharField("Marca/Modelo", max_length=100)
    ano_fabricacao = models.PositiveIntegerField("Ano de Fabricação")
    placa = models.CharField("Placa", max_length=8)
    cor = models.CharField("Cor", max_length=30)
    capacidade_carga = models.CharField("Capacidade de Carga (kg ou m³)", max_length=50)

    # Financeiro
    banco = models.CharField("Banco", max_length=100)
    agencia = models.CharField("Agência", max_length=20)
    conta = models.CharField("Conta", max_length=20)
    tipo_conta = models.CharField("Tipo de Conta", max_length=2, choices=TIPO_CONTA_CHOICES)
    pix = models.CharField("Chave PIX (se diferente da conta)", max_length=100, blank=True, null=True)

    # Outros
    cidade_base = models.CharField("Cidade Base", max_length=100)
    disponibilidade = models.CharField("Disponibilidade", max_length=15, choices=DISPONIBILIDADE_CHOICES, default='DISPONIVEL')
    ultima_roteirizacao = models.DateField("Última Roteirização", blank=True, null=True)
    data_cadastro = models.DateTimeField("Data do Cadastro", auto_now_add=True)

    def __str__(self):
        return f"{self.nome_completo} - {self.placa}"
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