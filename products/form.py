from django import forms
from .models import Produto, Compra, CartaoDeCreditoDebito


class DateInput(forms.DateInput):
    input_type = 'date'

class ProdutForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'categoria', 'cor', 'tamanho_em_cm', 'preco', 'imagem']


class FormaDePagamento(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['forma_de_pagamento']


class Cartao(forms.ModelForm):
    class Meta:
        model = CartaoDeCreditoDebito
        fields = ['nome_no_cartao',
                  'numero_do_cartao',
                  'ano_data_de_expiracao',
				  'mes_data_de_expiracao',
                  'codigo_cvv',
                  ]
