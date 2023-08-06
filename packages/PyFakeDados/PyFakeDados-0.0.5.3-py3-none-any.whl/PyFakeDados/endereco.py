import random
from PyFakeDados.CONSTANTS import *
from PyFakeDados.logradouro import gerar_logradouro, gerar_logradouro_com_numero, gerar_numero
from PyFakeDados.bairro import gerar_bairro
from PyFakeDados.cep import gerar_cep
from PyFakeDados.municipio import gerar_municipio
from PyFakeDados.estado import gerar_estado, gerar_uf, busca_nome_uf
from PyFakeDados.utils import remover_acentos

def gerar_endereco(uf=None, force_ASCII=False, force_upper=False):

    endereco = {}

    if uf is None:
        uf = gerar_uf()

    logradouro = gerar_logradouro()
    numero = gerar_numero()
    bairro = gerar_bairro()
    estado = busca_nome_uf(uf)
    municipio = gerar_municipio(uf=uf)
    cep = gerar_cep(uf=uf)

    endereco["uf"] = uf
    endereco["estado"] = estado
    endereco["municipio"] = municipio
    endereco["cep"] = cep
    endereco["bairro"] = bairro
    endereco["logradouro"] = logradouro
    endereco["numero"] = numero

    if force_ASCII:
        for i in endereco:
            if isinstance(endereco[i], str):
                endereco[i] = remover_acentos(endereco[i])
    
    if force_upper:
        for i in endereco:
            if isinstance(endereco[i], str):
                endereco[i] = endereco[i].upper()

    return endereco