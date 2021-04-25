# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 00:23:26 2021

@author: Guilherme Mazanti
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.animation import FuncAnimation

from Piramide_Etaria import get_piramide_etaria
from Vacinados import get_vacinados

def get_vacinados_por_dia(df, dias_media = None):
  vacinados_por_dia = df.DATA_APLICACAO_VACINA.value_counts()
  vacinados_por_dia.sort_index(inplace = True)

  datas = np.arange(vacinados_por_dia.index[0],\
                    vacinados_por_dia.index[-1] + pd.Timedelta(1, unit = "day"),\
                    pd.Timedelta(1, unit = "day"))
  vacinados_por_dia = vacinados_por_dia.reindex(datas, fill_value = 0)
  if dias_media is not None:
    vacinados_media = vacinados_por_dia.rolling(dias_media,\
                                                min_periods = dias_media,\
                                                center = False,\
                                                closed = "both").mean()
    return vacinados_por_dia, vacinados_media
  return vacinados_por_dia

def plot_vacinados_por_dia(pd_vacinados, dias_media):
  dose1 = pd_vacinados[pd_vacinados.DOSE==1]
  dose2 = pd_vacinados[pd_vacinados.DOSE==2]
  vacinados_por_dia, vacinados_media = get_vacinados_por_dia(pd_vacinados, dias_media)
  vacinados_por_dia1, vacinados_media1 = get_vacinados_por_dia(dose1, dias_media)
  vacinados_por_dia2, vacinados_media2 = get_vacinados_por_dia(dose2, dias_media)

  fig, ax = plt.subplots(figsize = (5, 5))
  ax.set_position([0.125, 0.15, 0.95-0.125, 0.95-0.15])
  ax.grid(True)
  ax.set_axisbelow(True)
  ax.bar(vacinados_por_dia1.index, vacinados_por_dia1.values, label = "1ª dose", color = "C0")
  ax.bar(vacinados_por_dia2.index, vacinados_por_dia2.values,\
         bottom = vacinados_por_dia1[vacinados_por_dia2.index].values,\
         label = "2ª dose", color = "C1")
  ax.plot(vacinados_media, label = "Média ({} dias)".format(dias_media), color = "black")
  #ax.plot(vacinados_media1, label = "Média1 (14 dias)", color = "C2")
  #ax.plot(vacinados_media2, label = "Média2 (14 dias)", color = "C3")

  ax.set_title("Quantidade de vacinados por dia")
  ax.set_xlabel("Dia")
  ax.set_ylabel("Quantidade de vacinados")
  ax.legend()

  for t in ax.get_xticklabels():
    t.set_rotation(15)

  fig.savefig("Gráficos/Vacinados_por_dia_{}.png".format(pd.Timestamp.today().strftime("%Y_%m_%d")))

def plot_total_vacinados(pd_vacinados):
  dose1 = pd_vacinados[pd_vacinados.DOSE==1]
  dose2 = pd_vacinados[pd_vacinados.DOSE==2]

  #vacinados_por_dia = get_vacinados_por_dia(pd_vacinados, None)
  vacinados_por_dia1 = get_vacinados_por_dia(dose1, None)
  vacinados_por_dia2 = get_vacinados_por_dia(dose2, None)

  fig, ax = plt.subplots(figsize = (5, 5))
  ax.set_position([0.15, 0.15, 0.95-0.15, 0.95-0.15])
  ax.grid(True)
  ax.set_axisbelow(True)
  #ax.plot(vacinados_por_dia1.cumsum(), label = "1ª dose")
  #ax.plot(vacinados_por_dia2.cumsum(), label = "2ª dose")
  #ax.plot(vacinados_por_dia.cumsum(), label = "Total")
  ax.stackplot(vacinados_por_dia1.index, vacinados_por_dia1.cumsum().values, labels = ("1ª dose",))
  ax.stackplot(vacinados_por_dia2.index, vacinados_por_dia2.cumsum().values, labels = ("2ª dose",))
  ax.set_title("Evolução do total de vacinados")
  ax.set_xlabel("Dia")
  ax.set_ylabel("Total de vacinados")
  ax.legend(loc = "upper left")

  for t in ax.get_xticklabels():
    t.set_rotation(15)

  fig.savefig("Gráficos/Total_vacinados_{}.png".format(pd.Timestamp.today().strftime("%Y_%m_%d")))

def get_pd_por_idade(df):
  # Cálculo da idade
  nascimento = pd.DatetimeIndex(df.DATA_NASCIMENTO_PACIENTE)
  vacina = pd.DatetimeIndex(df.DATA_APLICACAO_VACINA)
  idade = vacina.year - nascimento.year
  idade -= np.logical_or(vacina.month < nascimento.month, np.logical_and(vacina.month == nascimento.month, vacina.day < nascimento.day))

  # Contagem por idade
  idades = idade.value_counts().sort_index()

  # Contagem por faixa etária de 10 anos, pegando os centenários em uma só categoria
  idades = idades.groupby(np.minimum(idades.index//10, 10)).sum()
  idades.index *= 10

  return idades

def plot_por_idade(pd_vacinados, pd_piramide):
  dose1 = pd_vacinados[pd_vacinados.DOSE==1]
  dose2 = pd_vacinados[pd_vacinados.DOSE==2]

  idades1 = get_pd_por_idade(dose1)
  idades2 = get_pd_por_idade(dose2)

  # Pirâmide etária com as mesmas faixas
  # Dados de 2010 ; somamos 10 anos a todo mundo
  censo2010 = pd.Series(index = pd_piramide.Idade_min.values + 10,\
                        data = (pd_piramide.Homens + pd_piramide.Mulheres).values)
  censo2010 = censo2010.groupby(np.minimum(censo2010.index//10, 10)).sum()
  censo2010.index *= 10


  # Figura: números absolutos
  fig, ax = plt.subplots(figsize = (5, 5))
  ax.set_position([0.2, 0.11, 0.95-0.2, 0.95-0.11])
  ax.grid(True)
  ax.set_axisbelow(True)
  ax.barh(idades1.index, idades1.values, height = 8, label = "1ª dose")
  ax.barh(idades2.index, idades2.values, height = 8, label = "2ª dose")
  ax.set_yticks(range(0, 110, 10))
  labels = ["{} a {}".format(i, i+9) for i in range(0, 100, 10)]
  labels.append("≥ 100")
  ax.set_yticklabels(labels)
  ax.set_ylabel("Faixa etária")
  ax.set_xlabel("Quantidade de vacinados")
  ax.set_title("Quantidade de vacinados por faixa etária")
  ax.legend()
  fig.savefig("Gráficos/Faixa_etaria_abs_{}.png".format(pd.Timestamp.today().strftime("%Y_%m_%d")))

  # Figura: números relativos
  fig, ax = plt.subplots(figsize = (5, 5))
  ax.set_position([0.2, 0.11, 0.95-0.2, 0.95-0.11])
  ax.grid(True)
  ax.set_axisbelow(True)
  ax.barh(idades1.index, (idades1 / censo2010 * 100).values, height = 8, label = "1ª dose")
  ax.barh(idades2.index, (idades2 / censo2010 * 100).values, height = 8, label = "2ª dose")
  ax.set_yticks(range(0, 110, 10))
  labels = ["{} a {}".format(i, i+9) for i in range(0, 100, 10)]
  labels.append("≥ 100")
  ax.set_yticklabels(labels)
  ax.set_xlim([0, 100])
  ax.set_ylabel("Faixa etária")
  ax.set_xlabel("Porcentagem de vacinados")
  ax.set_title("Porcentagem de vacinados por faixa etária")
  ax.legend()
  fig.savefig("Gráficos/Faixa_etaria_rel_{}.png".format(pd.Timestamp.today().strftime("%Y_%m_%d")))

def get_datas_finais(pd_vacinados, populacao_CM, dias_media):
  inicio = pd.Timestamp.today() - pd.Timedelta(dias_media, unit = "day")

  restantes_por_doses = populacao_CM - pd_vacinados.DOSE.value_counts()
  restantes = 2*populacao_CM - pd_vacinados.shape[0]

  media = (pd_vacinados.DATA_APLICACAO_VACINA >= inicio).sum() / dias_media
  media1 = np.logical_and(pd_vacinados.DATA_APLICACAO_VACINA >= inicio, pd_vacinados.DOSE==1).sum() / dias_media
  media2 = np.logical_and(pd_vacinados.DATA_APLICACAO_VACINA >= inicio, pd_vacinados.DOSE==2).sum() / dias_media

  dias_para_final = pd.Timedelta(restantes / media, unit = "day")
  dias_para_final1 = pd.Timedelta(restantes_por_doses.loc[1] / media1, unit = "day")
  dias_para_final2 = pd.Timedelta(restantes_por_doses.loc[2] / media2, unit = "day")

  data_final = pd.Timestamp.today() + dias_para_final
  data_final1 = pd.Timestamp.today() + dias_para_final1
  data_final2 = pd.Timestamp.today() + dias_para_final2
  return data_final, data_final1, data_final2

def plot_por_tipo_de_vacina(pd_vacinados):
  tipos = np.unique(pd_vacinados.IMUNOBIOLOGICO.values)

  fig, ax = plt.subplots(figsize = (5, 5))
  ax.set_position([0.15, 0.15, 0.95-0.15, 0.95-0.15])
  ax.grid(True)
  ax.set_axisbelow(True)
  for tipo in tipos:
    vacinados_tipo = get_vacinados_por_dia(pd_vacinados[pd_vacinados.IMUNOBIOLOGICO==tipo], None)
    ax.plot(vacinados_tipo.cumsum(), label = tipo)
  ax.legend()
  ax.set_xlabel("Dia")
  ax.set_ylabel("Total de doses aplicadas")
  ax.set_title("Total de doses aplicadas por tipo de vacina")

  for t in ax.get_xticklabels():
    t.set_rotation(15)

  fig.savefig("Gráficos/Total_por_tipo_{}.png".format(pd.Timestamp.today().strftime("%Y_%m_%d")))

def plot_Mazanti(pd_vacinados, inicio = pd.Timestamp(2021, 1, 21)):
  """
  Quantidade de pessoas da família Mazanti que foram vacinadas
  """
  Mazanti = pd_vacinados[pd_vacinados.NOME_PACIENTE.apply(lambda x: "MAZANTI" in x)]

  hoje = pd.Timestamp.today()

  dose = []
  dose.append(pd.Series(index = np.arange(inicio, hoje, pd.Timedelta(1, unit = "day")), dtype = int))
  dose.append(pd.Series(index = np.arange(inicio, hoje, pd.Timedelta(1, unit = "day")), dtype = int))

  for i in [1, 2]:
    for _, dia in Mazanti[Mazanti.DOSE==i].DATA_APLICACAO_VACINA.iteritems():
      dose[i-1][dia] += 1

  fig, ax = plt.subplots(figsize = (5, 5))
  ax.set_position([0.1, 0.15, 0.95-0.1, 0.95-0.15])
  ax.grid(True)
  ax.set_axisbelow(True)
  #ax.plot(vacinados_por_dia1.cumsum(), label = "1ª dose")
  #ax.plot(vacinados_por_dia2.cumsum(), label = "2ª dose")
  #ax.plot(vacinados_por_dia.cumsum(), label = "Total")
  for i in [0, 1]:
    ax.stackplot(dose[i].index, dose[i].cumsum().values, labels = ("{}ª dose".format(i+1),))
  ax.set_title("Evolução do total de Mazanti vacinados")
  ax.set_xlabel("Dia")
  ax.set_ylabel("Total de Mazanti vacinados")
  ax.legend(loc = "upper left")

  ymin, ymax = ax.get_ylim()
  ax.set_yticks(range(0, int(ymax)+1))

  for t in ax.get_xticklabels():
    t.set_rotation(15)

  fig.savefig("Gráficos/Mazanti_vacinados_{}.png".format(pd.Timestamp.today().strftime("%Y_%m_%d")))

def animacao_por_idade(pd_vacinados):
  inicio = min(pd_vacinados.DATA_APLICACAO_VACINA)
  umDia = pd.Timedelta(1, unit = "day")
  hoje = pd.Timestamp.today()

  dose1 = pd_vacinados[pd_vacinados.DOSE==1]
  dose2 = pd_vacinados[pd_vacinados.DOSE==2]

  x_max = max(get_pd_por_idade(dose1))

  fig, ax = plt.subplots(figsize = (5, 5))
  ax.set_position([0.2, 0.11, 0.95-0.2, 0.95-0.11])
  ax.grid(True)
  ax.set_axisbelow(True)
  bars1 = ax.barh(range(0, 110, 10), [0]*11, height = 8, label = "1ª dose")
  bars2 = ax.barh(range(0, 110, 10), [0]*11, height = 8, label = "2ª dose")
  ax.set_yticks(range(0, 110, 10))
  labels = ["{} a {}".format(i, i+9) for i in range(0, 100, 10)]
  labels.append("≥ 100")
  ax.set_yticklabels(labels)
  ax.set_ylabel("Faixa etária")
  ax.set_xlabel("Quantidade de vacinados")
  ax.set_title("Quantidade de vacinados por faixa etária")
  ax.legend()
  texto_dia = ax.text(1400, 0, inicio.strftime("%d/%m/%Y"),\
                      ha = "center", va = "center",\
                      bbox = {"boxstyle": "round", "facecolor": "white"})

  def init():
    ax.set_xlim([0, x_max])
    return bars1.patches + bars2.patches + [texto_dia]

  def update(dia):
    texto_dia.set_text(pd.to_datetime(dia).strftime("%d/%m/%Y"))
    df1 = get_pd_por_idade(dose1[dose1.DATA_APLICACAO_VACINA <= dia]).reindex(range(0, 110, 10), fill_value = 0)
    df2 = get_pd_por_idade(dose2[dose2.DATA_APLICACAO_VACINA <= dia]).reindex(range(0, 110, 10), fill_value = 0)
    for i, bar in enumerate(bars1.patches):
      bar.set_width(df1[10*i])
    for i, bar in enumerate(bars2.patches):
      bar.set_width(df2[10*i])
    return bars1.patches + bars2.patches + [texto_dia]

  ani = FuncAnimation(fig, update, frames = np.arange(inicio, hoje+umDia, umDia),\
                      init_func = init, blit = True, interval = 333, repeat_delay = 1000)
  ani.save("Gráficos/Animacao_por_idade_{}.mp4".format(pd.Timestamp.today().strftime("%Y_%m_%d")))
  return ani

if __name__ == "__main__":
  plt.close("all")
  populacao_CM = 31346 # Fonte : https://cidades.ibge.gov.br/brasil/sp/candido-mota/panorama
  pd_piramide = get_piramide_etaria()
  pd_vacinados = get_vacinados()

  print("Quantidade de doses aplicadas:", pd_vacinados.shape[0])
  doses = pd_vacinados.DOSE.value_counts()
  print("Quantidade de 1ªs doses aplicadas:", doses.loc[1], "({:.1f}%)".format(doses.loc[1]/populacao_CM * 100))
  print("Quantidade de 2ªs doses aplicadas:", doses.loc[2], "({:.1f}%)".format(doses.loc[2]/populacao_CM * 100))

  plot_vacinados_por_dia(pd_vacinados, 14)
  plot_por_idade(pd_vacinados, pd_piramide)
  plot_total_vacinados(pd_vacinados)
  plot_por_tipo_de_vacina(pd_vacinados)
  plot_Mazanti(pd_vacinados)
  data_final, data_final1, data_final2 = get_datas_finais(pd_vacinados, populacao_CM, 14)

  print(data_final, data_final1, data_final2)

  ani = animacao_por_idade(pd_vacinados)