# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 23:35:40 2021

@author: Guilherme Mazanti
"""

import re
import pandas as pd

def get_piramide_etaria():

  with open("Dados/IBGE_Piramide_Etaria_Candido_Mota_SP_2010.html", "r") as arquivo:
    dados = arquivo.read()

  re_dados = re.compile("<th[^>]*?>(.*?) anos</th>" + # Faixa etária
                        "<td[^>]*?>(.*?)</td>" + # Quantidade de homens
                        "<td[^>]*?><div[^>]*?></div><span[^>]*>(.*?)</span></td>" + # Porcentagem de homens
                        "<td[^>]*?><div[^>]*?></div><span[^>]*>(.*?)</span></td>" + # Porcentagem de mulheres
                        "<td[^>]*?>(.*?)</td>") # Quantidade de mulheres

  lista_dados = re_dados.findall(dados)


  lista_formatada = []
  for faixa_etaria, homens, homens_perc, mulheres_perc, mulheres in lista_dados:
    idades = re.findall("(\d*) a (\d*)", faixa_etaria)
    if idades:
      idades = (int(idades[0][0]), int(idades[0][1]))
    else:
      idades = (100, -1)
    lista_formatada.append((*idades,\
      int(homens.replace(".", "")),\
      int(mulheres.replace(".", "")),\
      float(homens_perc.replace(",", ".").replace("%", "")),\
      float(mulheres_perc.replace(",", ".").replace("%", ""))))


  return pd.DataFrame(data = lista_formatada, columns = ["Idade_min", "Idade_max", "Homens", "Mulheres", "Homens_perc", "Mulheres_perc"])
