from .models import User
# from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
def obter_usuario_logado(request) -> User:
    try:
        usr = User.objects.get(nome_usuario_id=request.user.pk)
    except ObjectDoesNotExist:
        usr = ''

    return usr

def listar_todos_usuarios(user)->list:
    '''
    Retorma dotos os uauarios menos a ADM que solicitou
    :param user:
    :return: list
    '''
    return User.objects.all()\
    .exclude(pk=user.id)

def definir_gerente(user:User) -> User:

    if not user.is_gerente:
      user.is_gerente = True
      user.save()

    else:
        user.is_gerente = False
        user.save()

    return user

def buscar_user_cep(user:User):
    return User.objects.filter(cep = user.cep)