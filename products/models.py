from django.db import models
from .constantes import CATEGORIAS, COR, STATUS_DA_COMPRA, FORMA_DE_PAGAMENTOS, EFETUADO
from users.models import User


# Create your models here.
class Produto(models.Model):
    nome = models.CharField('Nome Do Produto', max_length=200)
    preco = models.DecimalField('Preço em R$', max_digits=100, decimal_places=2)
    categoria = models.PositiveIntegerField('Categoria', choices=(CATEGORIAS))
    cor = models.PositiveIntegerField('Cor', choices=(COR))
    tamanho_em_cm = models.DecimalField('Tamanho em cm', null=True, max_digits=100, decimal_places=2)
    imagem = models.ImageField('Imagem do Produto', upload_to='produtos/imagens/')

    def __str__(self):
        return self.nome


class CartaoDeCreditoDebito(models.Model):
    nome_no_cartao = models.CharField('Nome No Cartao', max_length=100)
    numero_do_cartao = models.CharField('Número do Cartão', max_length=16)
    mes_data_de_expiracao = models.CharField('Mês ', max_length=2)
    ano_data_de_expiracao = models.CharField('Ano ', max_length=2)
    codigo_cvv = models.CharField('Código de segurança (CVV)', max_length=4)

    def __str__(self):
        return self.numero_do_cartao


class Boleto(models.Model):
    codigo = models.CharField('Número do Código de Barras', max_length=48)

    def __str__(self):
        return self.codigo

class Compra(models.Model):
    boleto = models.ForeignKey(Boleto, on_delete=models.CASCADE, related_name='Produto',
                               blank=True, null=True)
    cartao_de_credito_ou_debito = models.ForeignKey(CartaoDeCreditoDebito, on_delete=models.CASCADE, related_name='Produto',
                                                    blank=True, null=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='Produto')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='User')
    data_da_compra = models.DateTimeField('Data da Compra')
    forma_de_pagamento = models.PositiveIntegerField('Forma de Pagamento', choices=FORMA_DE_PAGAMENTOS)
    status_da_compra = models.PositiveIntegerField('Status da Compra', choices=STATUS_DA_COMPRA,
                                                   default=EFETUADO[0])

    def __str__(self):
        return self.produto.nome + '/' + self.usuario.nome
