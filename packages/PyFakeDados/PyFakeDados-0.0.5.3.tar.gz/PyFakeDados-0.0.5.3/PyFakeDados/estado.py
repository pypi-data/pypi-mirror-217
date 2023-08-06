import random
from PyFakeDados.CONSTANTS import ESTADOS, ESTADOS_SIGLAS, ESTADOS_SIGLAS_NOME

ESTADOS_COL_ID = 0
ESTADOS_COL_SIGLA = 1
ESTADOS_COL_NOME = 2

def gerar_uf():
    return random.choice(ESTADOS_SIGLAS)

def validar_uf(uf):
    return uf in ESTADOS_SIGLAS

def gerar_estado():
    return random.choice(ESTADOS)[ESTADOS_COL_NOME]

def busca_nome_uf(uf):
    if uf.upper() not in ESTADOS_SIGLAS:
        raise ValueError("UF inválida.")
    return ESTADOS_SIGLAS_NOME[uf.upper()]