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
def motoristas_view(request):
    return render(request, 'motoristas.html')  # Certifique-se de que existe um template motoristas.html

def cadastrar_motorista(request):
    # Lógica para cadastrar motorista
    return render(request, 'cadastrar_motorista.html')

def listar_motoristas(request):
    # Lógica para listar motoristas
    return render(request, 'listar_motoristas.html')
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
    coletas = Cotacao.objects.all()
    return render(request, 'listar_coletas.html', {'coletas': coletas})

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

def cadastrar_coleta(request):
    if request.method == 'POST':
        form = ColetaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_coletas')  # Redireciona para a lista de coletas após o cadastro
    else:
        form = ColetaForm()
    
    return render(request, 'cadastrar_coleta.html', {'form': form})