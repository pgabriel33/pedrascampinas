from django.contrib import admin
from .models import  Produto,Compra,CartaoDeCreditoDebito,Boleto
# Register your models here.
admin.site.register(Produto)
admin.site.register(Compra)
admin.site.register(CartaoDeCreditoDebito)
admin.site.register(Boleto)

