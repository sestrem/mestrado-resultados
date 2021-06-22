import sys
import math
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import style

sns.set()
style.use('ggplot')



def image_consumo_recursos(tipo_roleta):
  utilizacao_RCs = pd.read_csv('{}_utilizacao_RCs.csv'.format(tipo_roleta), skiprows=1)
  utilizacao_RCs.columns = ['i','qtde']
  utilizacao_RCs['unidade'] = utilizacao_RCs.qtde.diff()  # quanto foi consumido do RC em cada iteração
  utilizacao_RCs['unidade'] = utilizacao_RCs['unidade'] * -1 # transforma o valor em positivo

  x_data = range(0, utilizacao_RCs.shape[0])

  #fig, ax = plt.subplots(figsize=(30,10))
  x_size = math.floor(len(utilizacao_RCs) / 2)
  fig, ax = plt.subplots(figsize=(30,10))




  #ax.xaxis.set_ticks(utilizacao_RCs['i'])

  odds = [n for n in utilizacao_RCs['i'] if (n%4 == 0)]
  print(odds)
  ax.xaxis.set_ticks(odds)

  ax.plot(x_data, utilizacao_RCs['qtde'], label='Restando')
  ax.plot(x_data, utilizacao_RCs['unidade'], label='Consumidos')

  ax.set_title('Consumo dos Recursos')
  ax.legend()
  fig.savefig('{}_consumo-recursos.png'.format(tipo_roleta))

def image_qtde_ap_acumulado_por_iteracao(tipo_roleta):
  ap_acumulado = pd.read_csv("{}_all_qtde_vezes_AP_executada.csv".format(tipo_roleta))
  #print(ap_acumulado)  
  ap_acumulado.columns = ['iteracao', 'x1','x2','x3','x4']
  print(ap_acumulado)

  #fig, ax = plt.subplots()
  fig, ax = plt.subplots(figsize=(30,10))
#  ax.xaxis.set_ticks(ap_acumulado['iteracao'])

  odds = [n for n in ap_acumulado['iteracao'] if (n%4 == 0)]
  #print(odds)
  ax.xaxis.set_ticks(odds)


  x_data = range(0, ap_acumulado.shape[0])

  ax.plot(x_data, ap_acumulado['x1'], label='X1')
  ax.plot(x_data, ap_acumulado['x2'], label='X2')
  ax.plot(x_data, ap_acumulado['x3'], label='X3')
  ax.plot(x_data, ap_acumulado['x4'], label='X4')

  ax.set_title('Qtde AP acumulado')
  ax.legend()
  fig.savefig("{}_qtde-ap-acumulado-por-iteracao.png".format(tipo_roleta))


def image_qtde_ap_por_iteracao(tipo_roleta):
  ap_acumulado = pd.read_csv("{}_all_qtde_vezes_AP_executada.csv".format(tipo_roleta))
  #print(ap_acumulado)  
  ap_acumulado.columns = ['iteracao', 'x1','x2','x3','x4']
  #print(ap_acumulado)

  ap_acumulado['x1_iteracao'] = ap_acumulado.x1.diff()  # quanto foi consumido do RC em cada iteração
  ap_acumulado['x2_iteracao'] = ap_acumulado.x2.diff()  # quanto foi consumido do RC em cada iteração
  ap_acumulado['x3_iteracao'] = ap_acumulado.x3.diff()  # quanto foi consumido do RC em cada iteração
  ap_acumulado['x4_iteracao'] = ap_acumulado.x4.diff()  # quanto foi consumido do RC em cada iteração
  #print(ap_acumulado)

  
  fig, ax = plt.subplots(figsize=(30,10))
  
  x_data = range(0, ap_acumulado.shape[0])


  ax.set_ticks = ap_acumulado['iteracao']
  #odds = [n for n in ap_acumulado['iteracao'] if n%2]

  #ax.xaxis.set_ticks(ap_acumulado['iteracao'])
  odds = [n for n in ap_acumulado['iteracao'] if (n%4 == 0)]
  print(odds)
  ax.xaxis.set_ticks(odds)  
  #ax.xaxis.set_ticks(odds)

  ax.plot(x_data, ap_acumulado['x1_iteracao'], label='X1')
  ax.plot(x_data, ap_acumulado['x2_iteracao'], label='X2')
  ax.plot(x_data, ap_acumulado['x3_iteracao'], label='X3')
  ax.plot(x_data, ap_acumulado['x4_iteracao'], label='X4')

  ax.set_title('Qtde Ações por iteração')
  ax.legend()
  fig.savefig('{}_qtde-ap-por-iteracao.png'.format(tipo_roleta))  




def create_images(tipo_roleta):
  image_consumo_recursos(tipo_roleta)
  image_qtde_ap_acumulado_por_iteracao(tipo_roleta)
  image_qtde_ap_por_iteracao(tipo_roleta)

create_images('prioridade')
create_images('qtde')
create_images('aleatoria')




print("...fim...")
sys.exit()

