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
from rest_framework.views import APIView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Motorista, Cotacao, Agregado
from .forms import MotoristaForm, AgregadoForm
from django.db.models import Q
from django.db.models import Sum  
from .models import Financeiro
from .forms import FinanceiroForm
from django.utils import timezone  # Import para usar datas
from django.shortcuts import get_object_or_404
import requests
from django.http import JsonResponse
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.http import require_POST

from .models import TodosMotoristas, Cotacao, Roteirizacao
from .forms import TodosMotoristasForm
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

  #---------------------------------------//////////////////////////--------------------------------------
def cadastrar_clientes(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()  # Salva no banco de dados
           # messages.success(request, "Cliente cadastrado com sucesso!")
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

#---------------------------------------------------------/////---------------------------------------------
class MotoristaListView(ListView):
    model = Motorista
    template_name = 'motoristas/motorista_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        nome = self.request.GET.get('nome')
        cpf_cnpj = self.request.GET.get('cpf_cnpj')

        if nome:
            queryset = queryset.filter(nome__icontains=nome)
        if cpf_cnpj:
            queryset = queryset.filter(cpf_cnpj__icontains=cpf_cnpj)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        nome = self.request.GET.get('nome')
        cpf_cnpj = self.request.GET.get('cpf_cnpj')

        agregados = Agregado.objects.all()

        if nome:
            agregados = agregados.filter(nome_completo__icontains=nome)
        if cpf_cnpj:
            agregados = agregados.filter(cpf__icontains=cpf_cnpj)

        context['agregados'] = agregados
        return context

class MotoristaCreateView(CreateView):
    model = Motorista
    form_class = MotoristaForm  
    template_name = 'motoristas/motorista_create.html'
    success_url = reverse_lazy('motorista_list')


class MotoristaUpdateView(UpdateView):
    model = Motorista
    form_class = MotoristaForm  
    template_name = 'motoristas/motorista_create.html'
    success_url = reverse_lazy('motorista_list')

class MotoristaDeleteView(DeleteView):
    model = Motorista
    template_name = 'motoristas/motorista_confirm_delete.html'
    success_url = reverse_lazy('motorista_list')

#---------------------------------------------MOTORISTAS AGREGADOS-----------------------------------------
class MotoristaAgregadoCreateView(CreateView):
    model = Agregado
    form_class = AgregadoForm
    template_name = 'agregado/motorista_agregado.html'
    success_url = reverse_lazy('motorista_list')

class MotoristaAgregadoUpdateView(UpdateView):
    model = Agregado
    form_class = AgregadoForm
    template_name = 'agregado/motorista_agregado.html'
    success_url = reverse_lazy('motorista_list')

class MotoristaAgregadoDeleteView(SuccessMessageMixin, DeleteView):
    model = Agregado
    template_name = 'agregado/motorista_agregado_confirm_delete.html'
    success_url = reverse_lazy('motorista_list')
    success_message = "Motorista agregado excluído com sucesso!"
#-----------------------------------------------------------------------------------------------------------
def ordens_coleta_view(request):
    return render(request, 'ordens_coleta.html')  

def controle_coletas_view(request):
    placa = request.GET.get('placa')
    cliente = request.GET.get('cliente')
    status_coleta = request.GET.get('status_coleta')
    status_entrega = request.GET.get('status_entrega')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    coletas = Cotacao.objects.all()

    if placa:
        coletas = coletas.filter(veiculo__icontains=placa)
    if cliente:
        coletas = coletas.filter(cliente__nome_razaosocial__icontains=cliente)
    if data_inicio and data_fim:
        coletas = coletas.filter(data_coleta__range=[data_inicio, data_fim])
    if status_coleta:
        coletas = coletas.filter(status_coleta=status_coleta)
    if status_entrega:
        coletas = coletas.filter(status_entrega=status_entrega)

    total_coletas = coletas.count()
    coletas_realizadas = coletas.filter(status_coleta='realizada').count()
    coletas_pendentes = coletas.filter(status_coleta='pendente').count()
    coletas_nao_realizadas = coletas.filter(status_coleta='nao_realizada').count()

    entregas_realizadas = coletas.filter(status_entrega='realizada').count()
    entregas_pendentes = coletas.filter(status_entrega='pendente').count()

    #  últimas roteirizações
    roteirizacoes = Roteirizacao.objects.select_related('motorista').prefetch_related('coletas').order_by('-data')[:20]

    # Marcar se há pendências em cada roteirização
    for roteiro in roteirizacoes:
        roteiro.tem_pendencias = any(
            c.status_coleta != 'REALIZADA' or c.status_entrega != 'ENTREGUE'
            for c in roteiro.coletas.all()
        )

    context = {
        'coletas': coletas,
        'motoristas': Motorista.objects.all(),
        'total_coletas': total_coletas,
        'coletas_realizadas': coletas_realizadas,
        'coletas_pendentes': coletas_pendentes,
        'coletas_nao_realizadas': coletas_nao_realizadas,
        'entregas_realizadas': entregas_realizadas,
        'entregas_pendentes': entregas_pendentes,
        'roteirizacoes': roteirizacoes,
    }

    return render(request, 'controle_coletas.html', context)

#---------------------------------------------------------------------------------------------------------------
@require_POST
def atribuir_coletas(request):
    coleta_ids = request.POST.getlist('coletas_selecionadas')
    cpf_motorista = request.POST.get('cpf_motorista')

    if not coleta_ids or not cpf_motorista:
        return JsonResponse({'status': 'erro', 'mensagem': 'Dados incompletos'}, status=400)

    try:
       # Após salvar a roteirização e atribuir coletas
            motorista = TodosMotoristas.objects.get(cpf_cnpj=cpf_motorista)
            motorista.disponibilidade = 'INDISPONIVEL'
            motorista.save()

    except TodosMotoristas.DoesNotExist:
        return JsonResponse({'status': 'erro', 'mensagem': 'Motorista não encontrado'}, status=404)

    roteirizacao = Roteirizacao.objects.create(motorista=motorista)
    roteirizacao.coletas.add(*Cotacao.objects.filter(id__in=coleta_ids))

    return redirect('controle_coletas')
    #return JsonResponse({'status': 'sucesso'})

#---------------------------------------------------------------------------------------------------------------
def financeiro_view(request):
    return render(request, 'financeiro.html')  

def sobre_view(request):
    return render(request, 'sobre.html')  


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
    coletas = Cotacao.objects.all()  # padrão: mostra tudo

    filtro_por = request.GET.get('filtro_por')
    valor = request.GET.get('valor', '').strip()
    data_coleta = request.GET.get('data_coleta', '').strip()

    if filtro_por == 'cliente' and valor:
        coletas = coletas.filter(cliente__nome_razaosocial__icontains=valor)
    elif filtro_por == 'cidade' and valor:
        coletas = coletas.filter(cidade_origem__icontains=valor)
    elif filtro_por == 'data' and data_coleta:
        coletas = coletas.filter(data_coleta=data_coleta)

    return render(request, 'listar_coletas.html', {'coletas': coletas})

#--------------------------------------------------Editar Coleta-----------------------------------------------------------
def editar_coleta(request, id):
    coleta = get_object_or_404(Cotacao, id=id)

    if request.method == 'POST':
        form = ColetaForm(request.POST, instance=coleta)
        if form.is_valid():
            form.save()
            messages.success(request, "Coleta atualizada com sucesso.")
            return redirect('listar_coletas')
        else:
            messages.error(request, "Erro ao atualizar a coleta.")
    else:
        form = ColetaForm(instance=coleta)  

    return render(request, 'editar_coleta.html', {'form': form})
#-----------------------------------------------------Excluir Coleta------------------------------------------
def excluir_coleta(request, id):
    coleta = get_object_or_404(Cotacao, id=id)
    if request.method == 'POST':
        coleta.delete()
        return redirect('listar_coletas')
    return render(request, 'excluir_coleta.html', {'coleta': coleta})

# -----------------------------------------------------------Função auxiliar para calcular o valor do frete
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

            # Atribuir cliente (ForeignKey)
            cliente = form.cleaned_data['cliente']
            coleta.cliente = cliente

            # Endereço de origem
            coleta.cep_origem = form.cleaned_data['cep_origem']
            coleta.rua_origem = request.POST.get('rua_origem', '')
            coleta.numero_origem = request.POST.get('numero_origem', '')
            coleta.bairro_origem = request.POST.get('bairro_origem', '')
            coleta.cidade_origem = request.POST.get('cidade_origem', '')
            coleta.uf_origem = request.POST.get('uf_origem', '')

            # Endereço de destino
            coleta.cep_destino = form.cleaned_data['cep_destino']
            coleta.rua_destino = request.POST.get('rua_destino', '')
            coleta.numero_destino = request.POST.get('numero_destino', '')
            coleta.bairro_destino = request.POST.get('bairro_destino', '')
            coleta.cidade_destino = request.POST.get('cidade_destino', '')
            coleta.uf_destino = request.POST.get('uf_destino', '')

            # Calcular valor do frete
            coleta.valor_frete = calcular_valor_frete(
                coleta.cep_origem,
                coleta.cep_destino,
                coleta.peso,
                coleta.dimensoes,
                coleta.valor_carga,
                coleta.tipo_frete
            )

            coleta.save()
            #messages.success(request, f"Coleta cadastrada com sucesso! Valor do frete: R$ {coleta.valor_frete}")
            #messages.success(request, f"Coleta cadastrada com sucesso!")
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
#---------------------------------------------------Buscar por Cliente--------------------------------------------------------------------
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
# --------------------------------------------------BUSCA DE ENDEREÇO DE COLETA-----------------------------------------------------------
def buscar_enderecos_da_coleta(request, coleta_id):
    try:
        coleta = Cotacao.objects.select_related('cliente').get(id=coleta_id)
        data = {
            'cep_origem': coleta.cep_origem,
            'numero_origem': coleta.cliente.numero,
            'rua_origem': coleta.cliente.rua,
            'bairro_origem': coleta.cliente.bairro,
            'cidade_origem': coleta.cliente.cidade,
            'uf_origem': coleta.cliente.uf,
            'cep_destino': coleta.cep_destino,
            
        }
        return JsonResponse(data)
    except Cotacao.DoesNotExist:
        return JsonResponse({'erro': 'Coleta não encontrada'}, status=404)
#------------------------------------------------------------------------------------------------------------------------------------------  
#----------------------------------------------Gerar PDF----------------------------------------------------------------------------------
def gerar_pdf_coleta(request, coleta_id):
    coleta = Cotacao.objects.get(id=coleta_id)
    template_path = 'pdf/resumo_coleta.html'
    context = {'coleta': coleta}
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resumo_coleta.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF: %s' % pisa_status.err)
    return response
#-----------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------Criar Roteirazacao-------------------------------------------------------------------------
def criar_roteirizacao_view(request):
    tipo_filtro = request.GET.get('tipo_motorista', '')

    motoristas = TodosMotoristas.objects.all()
    if tipo_filtro:
        motoristas = motoristas.filter(tipo=tipo_filtro)

    # Filtrar coletas ainda não roteirizadas
    coletas_ja_usadas = Roteirizacao.objects.values_list('coletas__id', flat=True)
    coletas = Cotacao.objects.filter(status_coleta='PENDENTE').exclude(id__in=coletas_ja_usadas)

    return render(request, 'roteirizacao.html', {
        'motoristas_unificados': motoristas,
        'coletas': coletas,
    })
#-----------------------------------------------------------------------------------------------------------------------------------------
@require_POST
def finalizar_roteirizacao(request, roteiro_id):
    roteiro = get_object_or_404(Roteirizacao, id=roteiro_id)

    # Finaliza todas as coletas
    for coleta in roteiro.coletas.all():
        coleta.status_coleta = 'REALIZADA'
        coleta.status_entrega = 'ENTREGUE'
        coleta.save()

    # Torna o motorista disponível novamente
    motorista = roteiro.motorista
    motorista.disponibilidade = 'DISPONIVEL'
    motorista.save()

    return JsonResponse({'status': 'sucesso'})
#-----------------------------------------------------------------------------------------------------------------------------------------
class TodosMotoristasCreateView(CreateView):
    model = TodosMotoristas
    form_class = TodosMotoristasForm
    template_name = 'todosmotoristas/cad_td_motoristas.html'
    success_url = reverse_lazy('todosmotoristas_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos_pessoais'] = ['nome', 'tipo', 'cpf_cnpj', 'rg', 'orgao_emissor', 'data_emissao_rg', 'cnh', 'data_nascimento']
        context['campos_contato'] = ['telefone', 'celular', 'celular2', 'email']
        context['campos_endereco'] = ['cep', 'rua', 'numero', 'bairro', 'cidade', 'estado']
        context['campos_veiculo'] = ['tipo_de_veiculo', 'marca_modelo', 'ano_fabricacao', 'placa', 'cor', 'capacidade_carga', 'cidade_base', 'disponibilidade', 'ultima_roteirizacao']
        context['campos_financeiro'] = ['banco', 'agencia', 'conta', 'tipo_conta', 'pix']
        return context


class TodosMotoristasListView(ListView):
    model = TodosMotoristas
    template_name = 'todosmotoristas/listar_tdmotoristas.html'
    context_object_name = 'motoristas'

    def get_queryset(self):
        queryset = super().get_queryset()
        tipo = self.request.GET.get('tipo_motorista')
        if tipo in ['PR', 'AG']:
            queryset = queryset.filter(tipo=tipo)
        return queryset


class TodosMotoristasUpdateView(UpdateView):
    model = TodosMotoristas
    form_class = TodosMotoristasForm
    template_name = 'todosmotoristas/cad_td_motoristas.html'  # Pode usar o mesmo do cadastro
    success_url = reverse_lazy('listar_motoristas')

class TodosMotoristasDeleteView(DeleteView):
    model = TodosMotoristas
    template_name = 'todosmotoristas/confirmar_exclusao.html'
    success_url = reverse_lazy('listar_motoristas')