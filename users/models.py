from django.db import models
from django.contrib.auth.models import User
from . import constantes as cons


# Create your models here.

class User(models.Model):
    nome_usuario = models.OneToOneField(User, null=False, on_delete=models.PROTECT)
    nome = models.CharField(verbose_name='Nome', max_length=30)
    email = models.EmailField(verbose_name='Email',max_length=71, null=True)
    cpf = models.CharField(verbose_name='CPF', max_length=14)
    data_de_nascimento = models.DateField(verbose_name='Data de Nascimento' )
    genero = models.CharField(max_length=1, null=True, verbose_name='Sexo',
                              choices=(
                                  (cons.SEXO_MASCULINO[0], cons.SEXO_MASCULINO[1]),
                                  (cons.SEXO_FEMININO[0], cons.SEXO_FEMININO[1]),
                              )
                              )
    endereco = models.CharField(verbose_name='Endereço', max_length=50)
    observacao_endereco = models.CharField(verbose_name='Obs', max_length=50)
    cidade = models.CharField(verbose_name='Cidade', max_length=20)
    estado = models.CharField(verbose_name='Estado', max_length=20)
    cep = models.CharField(verbose_name='CEP', max_length=9)
    telefone = models.CharField(verbose_name='Telefone', max_length=13)
    celular = models.CharField(verbose_name='Celular', max_length=13)
    is_gerente = models.BooleanField(default=False)
    
    def __str__(self):
         return self.nome
