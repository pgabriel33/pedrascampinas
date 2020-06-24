from rest_framework.generics import get_object_or_404
from .form import FormUser
from .models import User
from . import utils
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .form import LoginForm
from django.contrib.auth import logout
from datetime import datetime

class register(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/register.html'

#cria as informações do usuario
def novo_user(request):
    if request.method == 'POST':
        form_user = FormUser(request.POST)
        if form_user.is_valid():
            post = form_user.save(commit=False)
            post.nome_usuario = request.user
            post.save()
            return redirect('/')

    contexto = {'form':FormUser() }
    return render(request,'users/cadastra_usuaria.html',contexto)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                   password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                        
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def sair(request):
    logout(request)
    return redirect('index')

@login_required
def gerenciar_usuario(request):

    busca = request.POST.get('buscar')
    filtro = request.POST.get('inputState')

    user = utils.obter_usuario_logado(request)
    contexto = {}
    if user.is_gerente:
        users = utils.listar_todos_usuarios(user)
        filtro = ['ID', 'Nome', 'E-Mail', 'Celular', 'Cidade', 'Estado', 'CEP', 'Administrador']
        contexto.update({'users':users,'filtro':filtro})

    return render(request, 'users/gerenciar_usuario.html',contexto)

@login_required
def excluir(request,pk):
    user = utils.obter_usuario_logado(request)
    if user.is_gerente:
        user_excuir = get_object_or_404(User,id=pk)
        user_excuir.delete()

    return redirect('gerenciar_usuario')

@login_required
def definir_gerente(request,pk):
    user = utils.obter_usuario_logado(request)
    print(pk)
    if user.is_gerente:
        gerent = get_object_or_404(User, id=pk)
        gerent = utils.definir_gerente(gerent)
        print(gerent.is_gerente)

    return redirect('gerenciar_usuario')

def editar(request,pk):
    user = utils.obter_usuario_logado(request)
    user_edit = get_object_or_404(User, pk=pk)
    if user.is_gerente:
        if request.method == 'POST':
            form = FormUser(request.POST, instance=user_edit)
            if form.is_valid:
                user_edit = form.save()
                return redirect('gerenciar_usuario')




    form = FormUser(instance=user_edit)
    data = user_edit.data_de_nascimento.strftime('%Y-%m-%d')
    return render(request,'users/cadastra_usuaria.html',{'form':form, 'data':data })
#
# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm(instance=post)
#     return render(request, 'blog/post_edit.html', {'form': form})