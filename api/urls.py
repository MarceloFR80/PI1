from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import ClienteCreateAPIView, CotacaoCreateAPIView, cadastrar_cotacao, CadastrarCotacaoView,  ClienteListAPIView, ClienteDetailAPIView
from .views import MotoristaListView, MotoristaCreateView, MotoristaUpdateView, MotoristaDeleteView, MotoristaAgregadoCreateView, MotoristaAgregadoUpdateView, MotoristaAgregadoDeleteView
from .views import consultar_endereco

urlpatterns = [


    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    # CORRETO
    path('buscar_cliente/', views.buscar_cliente, name='buscar_cliente'),


    #path('clientes/', ClienteListAPIView.as_view(), name='listar_clientes_api'),
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),

    path('clientes/cadastrar/', ClienteCreateAPIView.as_view(), name='cadastrar_cliente_api'),
    path('clientes/novo/', views.cadastrar_clientes, name='cadastrar_clientes'),  
    #path('clientes/<int:pk>/', ClienteDetailAPIView.as_view(), name='cliente_detail'),  # Rota para editar/deletar
    #path('clientes/cadastrar/', views.cadastrar_clientes, name='cadastrar_clientes'),

    path('motoristas/', MotoristaListView.as_view(), name='motorista_list'),  # URL para listar motoristas
    path('motoristas/add/', MotoristaCreateView.as_view(), name='motorista_create'),  # URL para criação de motorista
    path('motoristas/<int:pk>/edit/', MotoristaUpdateView.as_view(), name='motorista_update'),
    path('motoristas/<int:pk>/delete/', MotoristaDeleteView.as_view(), name='motorista_delete'),

    path('agregado/novo/', MotoristaAgregadoCreateView.as_view(), name='motorista_agregado_create'),
    path('agregado/<int:pk>/editar/', MotoristaAgregadoUpdateView.as_view(), name='motorista_agregado_update'),
    path('agregado/<int:pk>/excluir/', MotoristaAgregadoDeleteView.as_view(), name='motorista_agregado_delete'),


    path('cotacao/cadastrar/', views.cadastrar_cotacao, name='cadastrar_cotacao'),
    path('cotacao/', views.ListarCotacoesView.as_view(), name='listar_cotacao'),  # Para visualizar todas as cotações
    path('api/cotacao/cadastrar/', CotacaoCreateAPIView.as_view(), name='cadastrar_cotacao'),
    path('api/cotacao/cadastrar/', cadastrar_cotacao, name='cadastrar_cotacao'),
    
    path('coletas/', views.listar_coletas, name='listar_coletas'),
    path('coletas/<int:id>/editar/', views.editar_coleta, name='editar_coleta'),
    path('coletas/<int:id>/excluir/', views.excluir_coleta, name='excluir_coleta'),
    path('coletas/cadastrar/', views.cadastrar_coleta, name='cadastrar_coleta'),

    path('atribuir-coletas/', views.atribuir_coletas, name='atribuir_coletas'),

    path('ordens-coleta/', views.ordens_coleta_view, name='ordens_coleta'),  
    path('controle-coletas/', views.controle_coletas_view, name='controle_coletas'),
   
    path('sobre/', views.sobre_view, name='sobre'),  #  página "Sobre"

    # path('financeiro/', views.financeiro_view, name='financeiro'),  #  "financeiro"
    path('financeiro/', views.FinanceiroListView.as_view(), name='financeiro_list'),
    path('financeiro/new/', views.FinanceiroCreateView.as_view(), name='financeiro_create'),
    path('financeiro/<int:pk>/edit/', views.FinanceiroUpdateView.as_view(), name='financeiro_update'),
    path('financeiro/<int:pk>/delete/', views.FinanceiroDeleteView.as_view(), name='financeiro_delete'),

    path('endereco/<str:cep>/', consultar_endereco, name='consultar_endereco'),
    path('coletas/endereco/<int:coleta_id>/', views.buscar_enderecos_da_coleta, name='buscar_enderecos_da_coleta'),
    
    path('coletas/<int:coleta_id>/resumo_pdf/', views.gerar_pdf_coleta, name='resumo_pdf_coleta'),
    path('roteirizacao/criar/', views.criar_roteirizacao_view, name='criar_roteirizacao'),
    path('roteirizacao/criar/', views.criar_roteirizacao_view, name='criar_roteirizacao'),
    path('roteirizacao/atribuir/', views.atribuir_coletas, name='atribuir_coletas'),
]