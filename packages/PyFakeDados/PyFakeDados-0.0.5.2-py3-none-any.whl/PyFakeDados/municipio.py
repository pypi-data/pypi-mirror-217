import csv
import random
import os
from pathlib import Path
from PyFakeDados.estado import gerar_uf
from PyFakeDados.CONSTANTS import MUNICIPIOS, MUNICIPIOS_POR_ESTADO

def gerar_municipio(uf=None):

    if uf is None:
        uf = gerar_uf()

    if uf.upper() not in MUNICIPIOS_POR_ESTADO:
        raise ValueError("UF inválida.")
    
    municipios = MUNICIPIOS_POR_ESTADO[uf]
    municipio = random.choice(municipios)

    return municipio
