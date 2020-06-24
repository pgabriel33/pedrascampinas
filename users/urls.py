from . import views
from django.urls import path

urlpatterns = [
    path('cadastra/', views.register.as_view(),name='cadastra'),
    path('informacoes/', views.novo_user,name='informacoes'),
    path('login/',views.user_login, name='login'),
    path('gerenciar_usuario/',views.gerenciar_usuario, name='gerenciar_usuario'),
    path('excluir/<int:pk>/',views.excluir, name='excluir'),
    path('definir_gerente/<int:pk>/', views.definir_gerente, name='definir_gerente'),
    path('editar/<int:pk>/', views.editar, name='editar'),
    path('gerenciar_usuario/', views.gerenciar_usuario, name='gerenciar_usuario'),
   
]