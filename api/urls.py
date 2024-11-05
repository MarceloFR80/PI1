from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import ClienteCreateAPIView, CotacaoCreateAPIView, cadastrar_cotacao, CadastrarCotacaoView,  ClienteListAPIView, ClienteDetailAPIView

urlpatterns = [


    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),


    #path('clientes/', ClienteListAPIView.as_view(), name='listar_clientes_api'),
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),

    path('clientes/cadastrar/', ClienteCreateAPIView.as_view(), name='cadastrar_cliente_api'),
    path('clientes/novo/', views.cadastrar_clientes, name='cadastrar_clientes'),  # Exibe o template de cadastro
    #path('clientes/<int:pk>/', ClienteDetailAPIView.as_view(), name='cliente_detail'),  # Rota para editar/deletar
    #path('clientes/cadastrar/', views.cadastrar_clientes, name='cadastrar_clientes'),
    path('motoristas/', views.motoristas_view, name='motoristas'),  # Certifique-se de que a view motoristas_view existe
    path('cadastrar_motorista/', views.cadastrar_motorista, name='cadastrar_motorista'),
    path('listar_motoristas/', views.listar_motoristas, name='listar_motoristas'),

    path('cotacao/cadastrar/', views.cadastrar_cotacao, name='cadastrar_cotacao'),
    path('cotacao/', views.ListarCotacoesView.as_view(), name='listar_cotacao'),  # Para visualizar todas as cotações
    path('api/cotacao/cadastrar/', CotacaoCreateAPIView.as_view(), name='cadastrar_cotacao'),
    path('api/cotacao/cadastrar/', cadastrar_cotacao, name='cadastrar_cotacao'),
    
    path('coletas/', views.listar_coletas, name='listar_coletas'),
    path('coletas/<int:id>/editar/', views.editar_coleta, name='editar_coleta'),
    path('coletas/<int:id>/excluir/', views.excluir_coleta, name='excluir_coleta'),
    path('coletas/cadastrar/', views.cadastrar_coleta, name='cadastrar_coleta'),

    path('ordens-coleta/', views.ordens_coleta_view, name='ordens_coleta'),  # Certifique-se de que a view ordens_coleta_view existe
    path('controle-coletas/', views.controle_coletas_view, name='controle_coletas'),
    path('financeiro/', views.financeiro_view, name='financeiro'),  # Defina a URL e a view para "financeiro"
    path('sobre/', views.sobre_view, name='sobre'),  # Adicione esta linha para a página "Sobre"
]