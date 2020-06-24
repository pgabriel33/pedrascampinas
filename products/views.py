from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from .form import ProdutForm, FormaDePagamento, Cartao
from .models import Produto, Compra, CartaoDeCreditoDebito, Boleto
from users import utils
from datetime import datetime
from . import constantes as cons
from datetime import *
from users.models import User


# Create your views here.

def cadastra_produtos(request):
    context = {}

    if request.method == 'POST':
        produt = ProdutForm(request.POST, request.FILES)
        print(produt.errors)
        if produt.is_valid():
            produt.save()
        sucess = ['Produto Cadastrado Com Sucesso']
        context.update({'sucess': sucess})

    context.update({'form': ProdutForm()})
    return render(request, 'products/cadastrar.html', context)


def gerenciar(request):
    produtos = Produto.objects.all()
    context = {'produtos': produtos}

    return render(request, 'products/gerenciar_produto.html', context)


def excluir(request, pk):
    user = utils.obter_usuario_logado(request)
    if user.is_gerente:
        prod_excuir = Produto.objects.get(id=pk)
        prod_excuir.delete()

    return redirect('gerenciar_produtos')


def editar(request, pk):
    user = utils.obter_usuario_logado(request)
    prod_edit = Produto.objects.get(id=pk)
    if user.is_gerente:
        if request.method == 'POST':
            form = ProdutForm(request.POST, instance=prod_edit)
            if form.is_valid():
                prod_edit = form.save()
                return redirect('gerenciar_produtos')

    form = ProdutForm(instance=prod_edit)

    return render(request, 'products/cadastrar.html', {'form': form})


@login_required
def comprar(request, pk):
    user = utils.obter_usuario_logado(request)
    produto = Produto.objects.get(id=pk)
    data_compra = datetime.now()

    if request.method == 'POST':

        id_foma_de_pagamento = int(request.POST.get('forma_de_pagamento'))

        # nova compra
        nova_compra = Compra()
        nova_compra.usuario = user
        nova_compra.produto = produto
        nova_compra.data_da_compra = datetime.now()
        nova_compra.forma_de_pagamento = id_foma_de_pagamento

        if id_foma_de_pagamento in cons.BOLETO:
            boleto = Boleto()
            data_vencimento = data_compra + timedelta(days=7)
            data_vencimento.strftime("%m/%d/%Y")
            data_compra.strftime("%m/%d/%Y")

            print(nova_compra.produto.preco)
            boleto.codigo = 'http://www.sicadi.com.br/mhouse/boleto/boleto3.php?' \
                            'numero_banco=341-7&' \
                            'local_pagamento=PAG%C1VEL+EM+QUALQUER+BANCO+AT%C9+O+VENCIMENTO&' \
                            'cedente=Pedras+Campinas+Ltda&' \
                            'data_documento=' + data_compra.strftime("%m/%d/%Y") + '&' \
                                                                                   'numero_documento=DF+00113&' \
                                                                                   'especie=&' \
                                                                                   'aceite=N&' \
                                                                                   'data_processamento=' + data_compra.strftime(
                "%m/%d/%Y") + '&' \
                              'uso_banco=&' \
                              'carteira=179&' \
                              'especie_moeda=Real&' \
                              'quantidade=1&' \
                              'valor=' + str(nova_compra.produto.preco) + '&' \
                                                                          'vencimento=' + data_vencimento.strftime(
                "%m/%d/%Y") + '&' \
                              'agencia=0049&' \
                              'codigo_cedente=10201-5&' \
                              'meunumero=00010435&' \
                              'valor_documento=' + str(nova_compra.produto.preco) + '&' \
                                                                                    'instrucoes=Taxa+de+visita+de+suporte%0D%0AAp%F3s+o+vencimento+R%24+0%2C80+ao+dia&' \
                                                                                    'mensagem1=&' \
                                                                                    'mensagem2=&' \
                                                                                    'mensagem3=ATEN%C7%C3O%3A+N%C3O+RECEBER+AP%D3S+15+DIAS+DO+VENCIMENTO&' \
                                                                                    'sacado=&' \
                                                                                    'Submit=Enviar'
            # salvar boleto
            boleto.save()

            # salvar compra
            nova_compra.boleto = boleto
            # nova_compra.status_da_compra=cons.EFETUADO[0]

            nova_compra.save()

            return meus_pedido(request)


        else:
            form_cartao = Cartao(request.POST, request.FILES)
            # print(form_cartao.errors)
            # print(form_cartao.is_valid())
            if form_cartao.is_valid():
                cartao_salvo = form_cartao.save()
                print(cartao_salvo.id)

                nova_compra.cartao_de_credito_ou_debito = cartao_salvo
                nova_compra.save()
                # nova_compra.status_da_compra
                return meus_pedido(request)

    context = {'produto': produto, 'nome_user': user.nome, 'data': data_compra.strftime("%m/%d/%Y"),
               'forma_de_pagamento': FormaDePagamento(),
               'cartao': Cartao()}

    return render(request, 'products/comprar.html', context)


def confirmar_comprar(request, pk):
    user = utils.obter_usuario_logado(request)
    produto = Produto.objects.get(id=pk)
    comp = Compra(produto=produto, usuario=user)
    comp.save()
    return redirect('home')


def meus_pedido(request):
    user = utils.obter_usuario_logado(request)
    compras: Compra = Compra.objects.filter(usuario=user)

    context = {'compras': compras}

    return render(request, 'products/meus_pedidos.html', context)


def get_name_by_id(request):
    data = {
        'nome': False
    }

    pk = int(request.GET.get('pk', None))
    print(pk)

    for nome in cons.STATUS_DA_COMPRA:

        if pk == nome[0]:
            data['nome'] = nome[1]

    for nome in cons.FORMA_DE_PAGAMENTOS:
        if pk == nome[0]:
            data['nome'] = nome[1]

    return JsonResponse(data)


def gerenciar_dashboard(request):
    vendas = Compra.objects.all()
    total_de_vendas = len(vendas)
    total_de_produtos = len(Produto.objects.all())
    total_de_usuarios = len(User.objects.all())

    context = {'total_de_vendas': total_de_vendas,
               'total_de_produtos': total_de_produtos,
               'total_de_usuarios': total_de_usuarios,
               'vendas':vendas}

    return render(request, 'products/gerenciar_dashboard.html',context)
