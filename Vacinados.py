# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 00:04:45 2021

@author: Guilherme Mazanti
"""

import pandas as pd

def get_vacinados():

  pd_por_mes = [pd.read_excel("Dados/LISTA_01.01.2021_A_31.01.2021.xlsx"),\
                pd.read_excel("Dados/LISTA_01.02.2021_A_28.02.2021.xlsx"),\
                pd.read_excel("Dados/LISTA_01.03.2021_A_31.03.2021.xlsx"),\
                pd.read_excel("Dados/LISTA_01.04.2021_A_23.04.2021.xlsx")]
  pd_dados = pd.concat(pd_por_mes, ignore_index = True)

  pd_dados.DATA_NASCIMENTO_PACIENTE = pd.to_datetime(pd_dados.DATA_NASCIMENTO_PACIENTE, format = "%d/%m/%Y")
  pd_dados.DATA_APLICACAO_VACINA = pd.to_datetime(pd_dados.DATA_APLICACAO_VACINA, format = "%d/%m/%Y")
  pd_dados.DATA_VALIDADE_LOTE = pd.to_datetime(pd_dados.DATA_VALIDADE_LOTE, format = "%d/%m/%Y")
  pd_dados.DOSE = pd_dados.DOSE.str.extract(r"(\d)").astype(int)

  return pd_dados
