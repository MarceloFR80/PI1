from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer, TemplateHTMLRenderer
from .models import Cliente
from .serializers import ClienteSerializer
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ClienteForm, ColetaForm
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CotacaoSerializer
from .models import Cotacao  # Supondo que este seja o nome do modelo de cotação
from rest_framework.views import APIView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Motorista
from django.db.models import Sum  # Importar Sum
from .models import Financeiro
from .forms import FinanceiroForm
from django.utils import timezone  # Import para usar datas
from django.shortcuts import get_object_or_404
import requests
from django.http import JsonResponse
#-----------------------------------LOGIN--------------------------------------------------------
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
#-----------------------------------------------------------------------------------------------

def index(request):
    return render(request, 'index.html')

def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'listar_clientes.html', {'clientes': clientes})


# def listar_clientes(request):
    # Aqui você pode buscar os clientes do banco de dados e passar para o template
    #return render(request, 'listar_clientes.html')

# def cadastrar_clientes(request):
  #  return render(request, 'cadastrar_clientes.html')

  #---------------------------------------//////////////////////////--------------------------------------
def cadastrar_clientes(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()  # Salva no banco de dados
            messages.success(request, "Cliente cadastrado com sucesso!")
            return redirect('index')  # Redireciona após o sucesso
        else:
            messages.error(request, "Erro ao cadastrar cliente. Verifique os dados.")
    else:
        form = ClienteForm()
    return render(request, 'cadastrar_clientes.html', {'form': form})

class ClienteListAPIView(generics.ListAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ClienteCreateAPIView(generics.CreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

# View para editar e deletar clientes
class ClienteDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

#---------------------------------------------------------COTAÇÃO---------------------------------------------#
class CotacaoCreateAPIView(generics.CreateAPIView):
    queryset = Cotacao.objects.all()
    serializer_class = CotacaoSerializer
   
class ListarCotacoesView(generics.ListAPIView):
    queryset = Cotacao.objects.all()
    serializer_class = CotacaoSerializer

class CadastrarCotacaoView(APIView):
    def post(self, request, *args, **kwargs):
        print("Dados recebidos:", request.data)  # Exibe os dados recebidos
        
        serializer = CotacaoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "message": "Cotação cadastrada com sucesso"}, status=status.HTTP_201_CREATED)
        print("Erros de validação:", serializer.errors)  # Exibe erros, se houver
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def cadastrar_cotacao(request):
    serializer = CotacaoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "message": "Cotação cadastrada com sucesso"}, status=status.HTTP_201_CREATED)
    return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



#class ListarCotacaoView(APIView):
    # def get(self, request, *args, **kwargs):
       # cotacoes = Cotacao.objects.all()
       # serializer = CotacaoSerializer(cotacoes, many=True)
        #return Response(serializer.data, status=status.HTTP_200_OK)

#---------------------------------------------------------/////---------------------------------------------
class MotoristaListView(ListView):
    model = Motorista
    template_name = 'motoristas/motorista_list.html'

class MotoristaCreateView(CreateView):
    model = Motorista
    fields = ['nome', 'tipo', 'cpf_cnpj', 'telefone', 'email', 'tipo_de_veiculo', 'placa', 'celular']
    template_name = 'motoristas/motorista_create.html'
    success_url = reverse_lazy('motorista_list')

class MotoristaUpdateView(UpdateView):
    model = Motorista
    fields = ['nome', 'tipo', 'cpf_cnpj', 'telefone', 'email', 'tipo_de_veiculo', 'placa', 'celular']
    template_name = 'motoristas/motorista_create.html'
    success_url = reverse_lazy('motorista_list')

class MotoristaDeleteView(DeleteView):
    model = Motorista
    template_name = 'motoristas/motorista_confirm_delete.html'
    success_url = reverse_lazy('motorista_list')

#-----------------------------------------------------------------------------------------------------------
def ordens_coleta_view(request):
    return render(request, 'ordens_coleta.html')  # Crie o template ordens_coleta.html se ainda não existir

def controle_coletas_view(request):
    return render(request, 'controle_coletas.html')  # Crie o template controle_coletas.html

def financeiro_view(request):
    return render(request, 'financeiro.html')  # Certifique-se de ter o template financeiro.html

def sobre_view(request):
    return render(request, 'sobre.html')  # Certifique-se de ter o template sobre.html


#---------------------------------------------------EDITAR_CLIENTES--------------------------------------------#
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'editar_cliente.html', {'form': form})
#---------------------------------------------------EXCLUIR_CLIENTES------------------------------------------#
def excluir_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('listar_clientes')
    return render(request, 'confirmar_exclusao.html', {'cliente': cliente})
#------------------------------------------------LISTAR COTACÕES---------------------------------------------


def listar_coletas(request):
    TIPO_FRETE_MAP = {
        'EX': 'Expresso',
        'NO': 'Normal'
    }

    coletas = Cotacao.objects.all()

    # Traduz os valores de tipo_frete antes de enviar ao template
    for coleta in coletas:
        coleta.tipo_frete = TIPO_FRETE_MAP.get(coleta.tipo_frete, coleta.tipo_frete)

    return render(request, 'listar_coletas.html', {'coletas': coletas})


#-------------------------------------------------------------------------------------------------------------
def editar_coleta(request, id):
    coleta = get_object_or_404(Cotacao, id=id)
    # Adicione aqui o código para editar a coleta
    return render(request, 'editar_coleta.html', {'coleta': coleta})

def excluir_coleta(request, id):
    coleta = get_object_or_404(Cotacao, id=id)
    if request.method == 'POST':
        coleta.delete()
        return redirect('listar_coletas')
    return render(request, 'excluir_coleta.html', {'coleta': coleta})

# Função auxiliar para calcular o valor do frete
def obter_distancia_real(cep_origem, cep_destino):
    api_key = ""  # Substitua pela sua chave de API
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={cep_origem}&destinations={cep_destino}&region=br&key={api_key}"

    print(f"URL da API: {url}")  # Log da URL gerada
    try:
        response = requests.get(url)
        print(f"Status da resposta: {response.status_code}")  # Log do status da resposta
        data = response.json()
        print(f"Dados retornados: {data}")  # Log dos dados retornados

        # Verifica se a resposta foi bem-sucedida
        if data["status"] == "OK":
            distancia_metros = data["rows"][0]["elements"][0]["distance"]["value"]  # Em metros
            distancia_km = distancia_metros / 1000  # Converte para km
            print(f"Distância calculada: {distancia_km} km")  # Log da distância calculada
            return distancia_km
        else:
            error_message = data.get("error_message", "Resposta inválida")
            print(f"Erro na API: {error_message}")
            return None
    except Exception as e:
        print(f"Erro ao obter distância real: {e}")
        return None


def calcular_valor_frete(cep_origem, cep_destino, peso, dimensoes, valor_carga, tipo_frete):
    # Fatores de cálculo do frete (substitua conforme suas necessidades)
    taxa_base = 5.00  # Taxa base
    taxa_distancia = 0.05  # Taxa por quilômetro
    taxa_peso = 0.10  # Taxa por quilo
    taxa_dimensoes = 0.02  # Taxa por dimensão (exemplo)
    taxa_seguro = 0.01 if tipo_frete == 'EX' else 0.005  # Taxa de seguro para frete expresso ou normal

    # Obtenha a distância real entre os dois CEPs
    distancia_real = obter_distancia_real(cep_origem, cep_destino)
    if distancia_real is None:
        print("Erro: Distância real não pôde ser calculada. Usando distância padrão.")
        distancia_real = 0  # Ou uma distância padrão como fallback

    # Cálculos baseados na distância real
    custo_distancia = distancia_real * taxa_distancia
    custo_peso = float(peso) * taxa_peso
    custo_dimensoes = float(dimensoes) * taxa_dimensoes
    custo_seguro = float(valor_carga) * taxa_seguro

    # Cálculo final
    valor_frete = taxa_base + custo_distancia + custo_peso + custo_dimensoes + custo_seguro
    return round(valor_frete, 2)  # Arredonda o valor final


# View para cadastrar coleta e salvar valor do frete
def cadastrar_coleta(request):
    if request.method == 'POST':
        form = ColetaForm(request.POST)
        if form.is_valid():
            coleta = form.save(commit=False)

            # Não é necessário atribuir cliente manualmente — já está vindo no form
            # Basta garantir que o campo se chama "cliente" no formulário

            # Extrai dados para cálculo
            cep_origem = coleta.cep_origem
            cep_destino = coleta.cep_destino
            peso = coleta.peso
            dimensoes = coleta.dimensoes
            valor_carga = coleta.valor_carga
            tipo_frete = coleta.tipo_frete

            # Calcula o valor do frete
            coleta.valor_frete = calcular_valor_frete(
                cep_origem, cep_destino, peso, dimensoes, valor_carga, tipo_frete
            )

            # Salva a coleta com o cliente já associado
            coleta.save()

            messages.success(request, f"Coleta cadastrada com sucesso! Valor do frete: R$ {coleta.valor_frete}")
            return redirect('listar_coletas')
        else:
            messages.error(request, 'Erro ao cadastrar a coleta. Verifique os dados e tente novamente.')
    else:
        form = ColetaForm()

    return render(request, 'cadastrar_coleta.html', {'form': form})

#---------------------------------------------------------------FINANCEIRO--------------------------------------------------
class FinanceiroListView(ListView):
    model = Financeiro
    template_name = 'financeiro/financeiro_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_receitas = Financeiro.objects.filter(operacao='CR').aggregate(total=Sum('valor'))['total'] or 0
        total_despesas = Financeiro.objects.filter(operacao='DB').aggregate(total=Sum('valor'))['total'] or 0
        total_lucro_prejuiso = total_receitas - total_despesas
        
        context['total_receitas'] = total_receitas
        context['total_despesas'] = total_despesas
        context['total_lucro_prejuiso'] = total_lucro_prejuiso
        return context

class FinanceiroCreateView(CreateView):
    model = Financeiro
    form_class = FinanceiroForm
    template_name = 'financeiro/financeiro_form.html'
    success_url = reverse_lazy('financeiro_list')

class FinanceiroUpdateView(UpdateView):
    model = Financeiro
    fields = ['descricao', 'valor', 'data_operacao', 'operacao']
    template_name = 'financeiro/financeiro_form.html'
    success_url = reverse_lazy('financeiro_list')

class FinanceiroDeleteView(DeleteView):
    model = Financeiro
    template_name = 'financeiro/financeiro_confirm_delete.html'
    success_url = reverse_lazy('financeiro_list')
#------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------VIACEP----------------------------------------------------------------------------------
def consultar_endereco(request, cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({"erro": "CEP não encontrado"}, status=404)
#-----------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------Buscar por Clente--------------------------------------------------------------------
def buscar_cliente(request):
    cliente_id = request.GET.get('id')
    try:
        cliente = Cliente.objects.get(id=cliente_id)
        data = {
            'cep': cliente.cep,
            'rua': cliente.rua,
            'numero': cliente.numero,
            'bairro': cliente.bairro,
            'cidade': cliente.cidade,
            'uf': cliente.uf,
        }
        return JsonResponse(data)
    except Cliente.DoesNotExist:
        return JsonResponse({'erro': 'Cliente não encontrado.'})
#-----------------------------------------------------------------------------------------------------------------------------------------    