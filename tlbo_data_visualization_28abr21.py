import sys
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import style

sns.set()
style.use('ggplot')



def image_consumo_recursos():
  utilizacao_RCs = pd.read_csv('utilizacao_RCs.csv', skiprows=1)
  utilizacao_RCs.columns = ['i','qtde']
  utilizacao_RCs['unidade'] = utilizacao_RCs.qtde.diff()  # quanto foi consumido do RC em cada iteração
  utilizacao_RCs['unidade'] = utilizacao_RCs['unidade'] * -1 # transforma o valor em positivo

  x_data = range(0, utilizacao_RCs.shape[0])

  fig, ax = plt.subplots(figsize=(30,10))
  ax.xaxis.set_ticks(utilizacao_RCs['i'])

  ax.plot(x_data, utilizacao_RCs['qtde'], label='Restando')
  ax.plot(x_data, utilizacao_RCs['unidade'], label='Consumidos')

  ax.set_title('Consumo dos Recursos')
  ax.legend()
  fig.savefig('consumo-recursos.png')

def image_qtde_ap_acumulado_por_iteracao():
  ap_acumulado = pd.read_csv("all_qtde_vezes_AP_executada.csv")
  print(ap_acumulado)  
  ap_acumulado.columns = ['iteracao', 'x1','x2','x3','x4']
  print(ap_acumulado)

  #fig, ax = plt.subplots()
  fig, ax = plt.subplots(figsize=(30,10))
  ax.xaxis.set_ticks(ap_acumulado['iteracao'])

  x_data = range(0, ap_acumulado.shape[0])

  ax.plot(x_data, ap_acumulado['x1'], label='X1')
  ax.plot(x_data, ap_acumulado['x2'], label='X2')
  ax.plot(x_data, ap_acumulado['x3'], label='X3')
  ax.plot(x_data, ap_acumulado['x4'], label='X4')

  ax.set_title('Qtde AP acumulado')
  ax.legend()
  fig.savefig('qtde-ap-acumulado-por-iteracao.png')


def image_qtde_ap_por_iteracao():
  ap_acumulado = pd.read_csv("all_qtde_vezes_AP_executada.csv")
  print(ap_acumulado)  
  ap_acumulado.columns = ['iteracao', 'x1','x2','x3','x4']
  print(ap_acumulado)

  ap_acumulado['x1_iteracao'] = ap_acumulado.x1.diff()  # quanto foi consumido do RC em cada iteração
  ap_acumulado['x2_iteracao'] = ap_acumulado.x2.diff()  # quanto foi consumido do RC em cada iteração
  ap_acumulado['x3_iteracao'] = ap_acumulado.x3.diff()  # quanto foi consumido do RC em cada iteração
  ap_acumulado['x4_iteracao'] = ap_acumulado.x4.diff()  # quanto foi consumido do RC em cada iteração
  print(ap_acumulado)


  fig, ax = plt.subplots(figsize=(30,10))
  
  x_data = range(0, ap_acumulado.shape[0])


  #ax.set_ticks = ap_acumulado['iteracao']
  ax.xaxis.set_ticks(ap_acumulado['iteracao'])

  ax.plot(x_data, ap_acumulado['x1_iteracao'], label='X1')
  ax.plot(x_data, ap_acumulado['x2_iteracao'], label='X2')
  ax.plot(x_data, ap_acumulado['x3_iteracao'], label='X3')
  ax.plot(x_data, ap_acumulado['x4_iteracao'], label='X4')

  ax.set_title('Qtde Ações por iteração')
  ax.legend()
  fig.savefig('qtde-ap-por-iteracao.png')  

image_consumo_recursos()
image_qtde_ap_acumulado_por_iteracao()
image_qtde_ap_por_iteracao()
print("...fim...")
sys.exit()

utilizacao_RCs = pd.read_csv('utilizacao_RCs.csv', skiprows=1)
utilizacao_RCs.columns = ['i','qtde']
utilizacao_RCs['unidade'] = utilizacao_RCs.qtde.diff()
utilizacao_RCs['unidade'] = utilizacao_RCs['unidade'] * -1
print(utilizacao_RCs)

#utilizacao_RCs['somatorio'] = utilizacao_RCs['qtde'].cumsum()

create_image2(utilizacao_RCs, 'Consumo dos Recursos', 'consumo-recursos.png')


sys.exit()


fitness = pd.read_csv('all_fitness.csv', names=['x1', 'x2', 'x3', 'x4'], skiprows=1)
#create_image(fitness, 'Fitness', 'fitness.png')


limites = pd.read_csv('all_bounds.csv', names=['x1', 'x2', 'x3', 'x4'], skiprows=1)

figure, axis = plt.subplots(3, 1)
axis[0].plot(fitness)
axis[0].set_title("Fitness")
print(fitness.columns)
axis[0].legend(['x1', 'x2', 'x3', 'x4'], fontsize = 12)
axis[0].set_prop_cycle('color', ['m', 'b', 'g','y'])
  
# For Cosine Function
axis[1].plot(qtde_vezes_AP)
axis[1].set_title("Qtde vezes AP foi executada")
axis[1].legend(['x1', 'x2', 'x3', 'x4'], fontsize = 12)

axis[2].plot(limites)
axis[2].set_title("Limites")
axis[2].legend(['x1', 'x2', 'x3', 'x4'], fontsize = 12)


plt.show()


# # setting style for graphs
# style.use('ggplot')
# plt.rcParams['figure.figsize'] = (20,10)


# fig2 = plt.plot(fitness.x1, label = 'X1')
# plt.legend(loc = 'upper left', fontsize = 12)
# plt.xticks(rotation = 90, color = 'black')
# plt.yticks(color = 'black')
# plt.title('Immigration to Canada from 1980-2013',color = 'black')
# plt.xlabel('Year',color = 'black')
# plt.ylabel('Number of Immigrants',color = 'black')
# plt.savefig('linechart_multiple.png')

# plt.show()


def create_image2(df, title, file_name):
  print(df.head(100))
  

  columns = df.columns
  print(columns)
  # create x data
  x_data = range(0, df.shape[0])
  print(x_data)
# create figure and axis
  fig, ax = plt.subplots()
# plot each column
  # for column in columns:
  #     ax.plot(x_data, df[column], label=column)

  ax.plot(x_data, df['qtde'], label='Restando')
  ax.plot(x_data, df['unidade'], label='Consumidos')
#  ax.plot(x_data, df['somatorio'], label='somatorio')  
# set title and legend
  ax.set_title(title)
  ax.legend()
  fig.savefig(file_name)



def create_image(df, title, file_name):
  print(df.head())

  columns = df.columns
  print(columns)
  # create x data
  x_data = range(0, df.shape[0])
  print(x_data)
# create figure and axis
  fig, ax = plt.subplots()
# plot each column
  for column in columns:
      ax.plot(x_data, df[column], label=column)
# set title and legend
  ax.set_title(title)
  ax.legend()
  fig.savefig(file_name)  