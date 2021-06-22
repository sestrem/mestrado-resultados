import sys
import math
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import style

sns.set()
style.use('ggplot')


def teste():
  x = np.array([0,1,2,3])
  y = np.array([0.650, 0.660, 0.675, 0.685])
  my_xticks = ['a', 'b', 'c', 'd']
  plt.xticks(x, my_xticks)
  plt.yticks(np.arange(y.min(), y.max(), 0.005))
  plt.plot(x, y)
  plt.grid(axis='y', linestyle='-')
  plt.show()

def image_consumo_recursos(tipo_roleta):
  utilizacao_RCs = pd.read_csv('{}_utilizacao_RCs.csv'.format(tipo_roleta), skiprows=0)
  # print(utilizacao_RCs)
  utilizacao_RCs.columns = ['i','qtde']
  # print(utilizacao_RCs)

  utilizacao_RCs['unidade'] = utilizacao_RCs.qtde.diff()  * -1 # quanto foi consumido do RC em cada iteração (# transforma o valor em positivo)
  utilizacao_RCs['unidade'] = utilizacao_RCs['unidade']  
  
  x_data = range(0, utilizacao_RCs.shape[0])

  plt.bar(x_data, utilizacao_RCs['unidade'], alpha=0.2)
  plt.plot(x_data, utilizacao_RCs['qtde'])
  plt.xticks(x_data, np.arange(0,utilizacao_RCs.shape[0],1))
  plt.legend(['Restando','Consumidos'])

  plt.title('Consumo dos Recursos')
  
  plt.savefig('{}_consumo-recursos.png'.format(tipo_roleta))
  




def image_qtde_ap_acumulado_por_ciclo(tipo_roleta):
  ap_acumulado = pd.read_csv("{}_all_qtde_vezes_AP_executada.csv".format(tipo_roleta))
  
  ap_acumulado.columns = ['ciclo', 'x1','x2','x3','x4']

  ap_acumulado['x1_ciclo'] = ap_acumulado.x1.diff()  # quanto foi consumido do RC em cada ciclo
  ap_acumulado['x2_ciclo'] = ap_acumulado.x2.diff()  # quanto foi consumido do RC em cada ciclo
  ap_acumulado['x3_ciclo'] = ap_acumulado.x3.diff()  # quanto foi consumido do RC em cada ciclo
  ap_acumulado['x4_ciclo'] = ap_acumulado.x4.diff()  # quanto foi consumido do RC em cada ciclo  
  #print(ap_acumulado)


  ap_acumulado['x1_ciclo'].fillna(ap_acumulado['x1'], inplace=True)
  ap_acumulado['x2_ciclo'].fillna(ap_acumulado['x2'], inplace=True)
  ap_acumulado['x3_ciclo'].fillna(ap_acumulado['x3'], inplace=True)
  ap_acumulado['x4_ciclo'].fillna(ap_acumulado['x4'], inplace=True)

  ap_acumulado['somatorio'] = ap_acumulado['x1_ciclo'] + ap_acumulado['x2_ciclo'] + ap_acumulado['x3_ciclo'] + ap_acumulado['x4_ciclo']

  ap_acumulado['x1_percentual'] = (ap_acumulado['x1_ciclo']*100)/ap_acumulado['somatorio']
  ap_acumulado['x2_percentual'] = (ap_acumulado['x2_ciclo']*100)/ap_acumulado['somatorio']
  ap_acumulado['x3_percentual'] = (ap_acumulado['x3_ciclo']*100)/ap_acumulado['somatorio']
  ap_acumulado['x4_percentual'] = (ap_acumulado['x4_ciclo']*100)/ap_acumulado['somatorio']

  #fig, ax = plt.subplots()
  fig, ax = plt.subplots(figsize=(30,10))
#  ax.xaxis.set_ticks(ap_acumulado['iteracao'])


  ax.xaxis.set_ticks(np.arange(0,ap_acumulado.shape[0],1))

  x_data = range(0, ap_acumulado.shape[0])

  # create plot
  fig, ax = plt.subplots()
#  index = np.arange(ap_acumulado.shape[0] + 1)
  index = np.arange(ap_acumulado.shape[0])
  # print(index)
  
  bar_width = 0.2
  opacity = 0.8

  rects1 = plt.bar(index, ap_acumulado['x1_percentual'], bar_width,
  alpha=opacity,
  color='b',
  label='X1')

  rects2 = plt.bar(index + bar_width, ap_acumulado['x2_percentual'], bar_width,
  alpha=opacity,
  color='g',
  label='X2')

  rects3 = plt.bar(index + (bar_width * 2), ap_acumulado['x3_percentual'], bar_width,
  alpha=opacity,
  color='r',
  label='X3')

  rects4 = plt.bar(index + (bar_width*3), ap_acumulado['x4_percentual'], bar_width,
  alpha=opacity,
  color='y',
  label='X4')

  __autolabel(ax, rects1)
  __autolabel(ax, rects2)
  __autolabel(ax, rects3)
  __autolabel(ax, rects4)  

  plt.xlabel('Ciclo')
  plt.ylabel('%')
  plt.title('% ações por ciclo', loc='left')
  plt.xticks(x_data, np.arange(1,ap_acumulado.shape[0]+1,1))
  
  plt.legend(['X1', 'X2', 'X3', 'X4'])

  plt.tight_layout()
  #plt.show()

  plt.savefig("{}_percentual-ap-por-ciclo.png".format(tipo_roleta))
  
  
  


def image_qtde_ap_por_ciclo(tipo_roleta):
  ap_acumulado = pd.read_csv("{}_all_qtde_vezes_AP_executada.csv".format(tipo_roleta))
  #print(ap_acumulado)  
  ap_acumulado.columns = ['ciclo', 'x1','x2','x3','x4']
  # print(ap_acumulado)

  ap_acumulado['x1_ciclo'] = ap_acumulado.x1.diff()  # quanto foi consumido do RC em cada iteração
  ap_acumulado['x2_ciclo'] = ap_acumulado.x2.diff()  # quanto foi consumido do RC em cada iteração
  ap_acumulado['x3_ciclo'] = ap_acumulado.x3.diff()  # quanto foi consumido do RC em cada iteração
  ap_acumulado['x4_ciclo'] = ap_acumulado.x4.diff()  # quanto foi consumido do RC em cada iteração
  #print(ap_acumulado)

  ap_acumulado['somatorio'] = ap_acumulado['x1_ciclo'] + ap_acumulado['x2_ciclo'] + ap_acumulado['x3_ciclo'] + ap_acumulado['x4_ciclo']
  #print(ap_acumulado)
  
  ap_acumulado['x1_percentual'] = (ap_acumulado['x1_ciclo']*100)/ap_acumulado['somatorio']
  ap_acumulado['x2_percentual'] = (ap_acumulado['x2_ciclo']*100)/ap_acumulado['somatorio']
  ap_acumulado['x3_percentual'] = (ap_acumulado['x3_ciclo']*100)/ap_acumulado['somatorio']
  ap_acumulado['x4_percentual'] = (ap_acumulado['x4_ciclo']*100)/ap_acumulado['somatorio']
  # print(ap_acumulado)
  
  fig_qtde, ax_qtde = plt.subplots(figsize=(30,10))
  
  x_data = range(0, ap_acumulado.shape[0])

  

  #odds = [n for n in ap_acumulado['iteracao'] if n%2]

  #ax.xaxis.set_ticks(ap_acumulado['iteracao'])
  # odds = [n for n in ap_acumulado['iteracao'] if (n%4 == 0)]
  # #print(odds)
  # ax.xaxis.set_ticks(odds)  
  #ax.xaxis.set_ticks(odds)

  # print(ap_acumulado)
  # print(ap_acumulado['x1_percentual'])

  # print(ap_acumulado['x1_percentual'].min())
  # y_min = min(ap_acumulado['x1_percentual'].min, ap_acumulado['x2_percentual'].min, ap_acumulado['x3_percentual'].min, ap_acumulado['x4_percentual'].min)
  # y_max = max(ap_acumulado['x1_percentual'], ap_acumulado['x2_percentual'], ap_acumulado['x3_percentual'], ap_acumulado['x4_percentual'])
  # ax.set_yticks(np.arange(0, 100, 10))
  ax_qtde.plot(x_data, ap_acumulado['x1_percentual'], label='X1')
  ax_qtde.plot(x_data, ap_acumulado['x2_percentual'], label='X2')
  ax_qtde.plot(x_data, ap_acumulado['x3_percentual'], label='X3')
  ax_qtde.plot(x_data, ap_acumulado['x4_percentual'], label='X4')
  ax_qtde.set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
  #ax.set_yticks(np.arange(0, 100, 10))

  # print(len(ap_acumulado))
  ax_qtde.set_xticks(np.arange(1, len(ap_acumulado)-1, 1))

  ax_qtde.set_title('% Ações por ciclo')
  ax_qtde.legend()
  fig_qtde.savefig('{}_qtde-ap-por-ciclo.png'.format(tipo_roleta))  


def __autolabel(ax, rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom', fontsize='x-large')

def image_valor_ap_por_ciclo(tipo_roleta):
  ap_fitness = pd.read_csv("{}_all_fitness.csv".format(tipo_roleta))

  ap_fitness.columns = ['ciclo', 'x1','x2','x3','x4']
  fig, ax = plt.subplots(figsize=(30,10))
  
  x_data = range(0, ap_fitness.shape[0])

  # ax.plot(x_data, ap_fitness['x1'],'ro-', label='X1')
  # ax.plot(x_data, ap_fitness['x2'], label='X2')
  # ax.plot(x_data, ap_fitness['x3'], label='X3')
  # ax.plot(x_data, ap_fitness['x4'], label='X4')
  index = np.arange(ap_fitness.shape[0])
  # print(index)
  
  bar_width = 0.2
  opacity = 0.8
  rects1 = plt.bar(index, ap_fitness['x1'], bar_width,
  alpha=opacity,
  color='b',
  label='X1')

  rects2 = plt.bar(index + bar_width, ap_fitness['x2'], bar_width,
  alpha=opacity,
  color='g',
  label='X2')

  rects3 = plt.bar(index + (bar_width * 2), ap_fitness['x3'], bar_width,
  alpha=opacity,
  color='r',
  label='X3')

  rects4 = plt.bar(index + (bar_width*3), ap_fitness['x4'], bar_width,
  alpha=opacity,
  color='y',
  label='X4')

  # for tick in ax.xaxis.get_minor_ticks():
  #     tick.tick1line.set_markersize(0)
  #     tick.tick2line.set_markersize(0)
  #     tick.label1.set_horizontalalignment('center')  

  __autolabel(ax, rects1)
  __autolabel(ax, rects2)
  __autolabel(ax, rects3)
  __autolabel(ax, rects4)



  plt.xticks(x_data, np.arange(1, ap_fitness.shape[0]+1,  1),fontsize=16)
  plt.legend(['X1', 'X2', 'X3', 'X4'])  
  ax.set_title('Valor das ações positivas por ciclo')
  ax.legend()
  fig.savefig('{}_valor-ap-por-ciclo.png'.format(tipo_roleta))    

def create_images(tipo_roleta):
  #teste2(tipo_roleta)
  #image_qtde_ap_por_ciclo(tipo_roleta)
  image_consumo_recursos(tipo_roleta)
  image_qtde_ap_acumulado_por_ciclo(tipo_roleta)
  image_valor_ap_por_ciclo(tipo_roleta)


# print('Number of arguments:', len(sys.argv), 'arguments.')
# print('Argument List:', str(sys.argv))
#teste()
if len(sys.argv) > 1:
  print(sys.argv[1])
  create_images(sys.argv[1])
else:
  # create_images('prioridade')
  # create_images('qtde')
  # create_images('aleatoria')
  create_images('valor')




print("...fim...")
sys.exit()

##############
def ___image_consumo_recursos(tipo_roleta):
  utilizacao_RCs = pd.read_csv('{}_utilizacao_RCs.csv'.format(tipo_roleta), skiprows=0)
  
  utilizacao_RCs.columns = ['i','qtde']
  utilizacao_RCs['unidade'] = utilizacao_RCs.qtde.diff()  # quanto foi consumido do RC em cada iteração
  utilizacao_RCs['unidade'] = utilizacao_RCs['unidade'] * -1 # transforma o valor em positivo

  x_data = range(0, utilizacao_RCs.shape[0])
  print(x_data)
  #fig, ax = plt.subplots(figsize=(30,10))
  x_size = math.floor(len(utilizacao_RCs) / 2)
  fig, ax = plt.subplots(figsize=(30,10))




  #ax.xaxis.set_ticks(utilizacao_RCs['i'])

  # odds = [n for n in utilizacao_RCs['i'] if (n%4 == 0)]
  odds = [n for n in utilizacao_RCs['i']]
  print(odds)
  #ax.xaxis.set_ticks(odds)

  ax.plot(x_data, utilizacao_RCs['qtde'], label='Restando')
  ax.plot(x_data, utilizacao_RCs['unidade'], label='Consumidos')

  ax.set_title('Consumo dos Recursos')
  ax.legend()
  fig.savefig('{}_consumo-recursos.png'.format(tipo_roleta))


def ____image_qtde_ap_acumulado_por_iteracao(tipo_roleta):
  ap_acumulado = pd.read_csv("{}_all_qtde_vezes_AP_executada.csv".format(tipo_roleta))
  #print(ap_acumulado)  
  ap_acumulado.columns = ['iteracao', 'x1','x2','x3','x4']
  #print(ap_acumulado)

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
