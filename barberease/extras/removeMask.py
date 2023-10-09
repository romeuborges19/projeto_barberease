import re


def remove_mask(numero):
    '''Funçâo responsavel por remover a mascara de um campo númerico'''

    numero = re.sub('[^0-9]', '', numero)
    return numero