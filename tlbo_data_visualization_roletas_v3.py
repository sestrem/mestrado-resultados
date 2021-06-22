import sys
import math
from notion.block import PageBlock
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import traceback
from matplotlib import style

from notion.client import *
from notion.block import *
from notion.collection import NotionDate


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

def image_consumo_recursos(tipo_roleta, prefixo):
  utilizacao_RCs = pd.read_csv('resultados/{}_{}_utilizacao_RCs.csv'.format(tipo_roleta, prefixo), skiprows=0)
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
  
  plt.savefig('resultados/{}_{}_consumo-recursos.png'.format(tipo_roleta, prefixo))
  




def image_qtde_ap_acumulado_por_ciclo(tipo_roleta, prefixo):
  ap_acumulado = pd.read_csv("resultados/{}_{}_all_qtde_vezes_AP_executada.csv".format(tipo_roleta, prefixo))
  
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

  plt.savefig("resultados/{}_{}percentual-ap-por-ciclo.png".format(tipo_roleta, prefixo))
  
  
  


def image_qtde_ap_por_ciclo(tipo_roleta):
  ap_acumulado = pd.read_csv("resultados/{}_all_qtde_vezes_AP_executada.csv".format(tipo_roleta))
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
  fig_qtde.savefig('resultados/{}_qtde-ap-por-ciclo.png'.format(tipo_roleta))  


def __autolabel(ax, rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        if math.isnan(height):
          continue
        w = rect.get_x() + rect.get_width()/2.
        ax.text(w, 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom', fontsize='x-large')

def image_valor_ap_por_ciclo(tipo_roleta, prefixo):
  ap_fitness = pd.read_csv("resultados/{}_{}_all_fitness.csv".format(tipo_roleta, prefixo))

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
  fig.savefig('resultados/{}_{}_valor-ap-por-ciclo.png'.format(tipo_roleta, prefixo))    

def create_images(tipo_roleta, prefixo):
  #teste2(tipo_roleta)
  #image_qtde_ap_por_ciclo(tipo_roleta)
  image_consumo_recursos(tipo_roleta, prefixo)
  image_qtde_ap_acumulado_por_ciclo(tipo_roleta, prefixo)
  image_valor_ap_por_ciclo(tipo_roleta, prefixo)


# print('Number of arguments:', len(sys.argv), 'arguments.')
# print('Argument List:', str(sys.argv))
#teste()
# if len(sys.argv) > 1:
#   print(sys.argv[1])
#   create_images(sys.argv[1])
# else:


def teste_notion():
    token_v2 = "9a07de97da77103b6b40ad24445a064c18f9e9a5a700154140104699b5971854aaffe9fc9dd4bc6aaa9858f7e883c7b053484adefdcde2d416ed38f6d8af110a6ba263a4025d1bb9a6b8bdb688dd"
    notion_client = NotionClient(token_v2=token_v2)

    #global notion_client
    url="https://www.notion.so/24-05-2021-6d11acf4f3b44b868be082ddcacc21d4"

    page = notion_client.get_block(url, limit=10)

    new_page = page.children.add_new(PageBlock, title="19/05/2021")
    newchild = new_page.children.add_new(EmbedOrUploadBlock, title="resultado")
    newchild.upload_file("prioridade_c1__qtde[1500.00 200.00 150.00 150.00]__prioridade[25.00 25.00 25.00 25.00]_consumo-recursos.png")    

# teste_notion()
# print("teste Notion finalizado")


prefixo = ""
if len(sys.argv) > 1:
  prefixo = sys.argv[1]

#prefixo = "c1__qtde[1500.00 200.00 150.00 150.00]__prioridade[25.00 25.00 25.00 25.00]"


def image_consumo_recursos2(prefixo_file):
  utilizacao_RCs = pd.read_csv('resultados/{}_utilizacao_RCs.csv'.format(prefixo_file), skiprows=0)
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
  
  file_name_img = 'resultados/{}_consumo-recursos.png'.format(prefixo_file)
  plt.savefig(file_name_img)
  plt.close()
  return file_name_img

def image_valor_ap_por_ciclo2(prefixo_file):
  ap_fitness = pd.read_csv("resultados/{}_all_fitness.csv".format(prefixo_file), skiprows=0)

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
  file_name_img = 'resultados/{}_valor-ap-por-ciclo.png'.format(prefixo_file)
  fig.savefig(file_name_img)  
  plt.close()
  return file_name_img

def image_qtde_ap_acumulado_por_ciclo2(prefixo_file):
  print("resultados/{}_all_qtde_vezes_AP_executada.csv".format(prefixo_file))
  ap_acumulado = pd.read_csv("resultados/{}_all_qtde_vezes_AP_executada.csv".format(prefixo_file), skiprows=0)
  
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

  file_name_img = "resultados/{}_percentual-ap-por-ciclo.png".format(prefixo_file)
  plt.savefig(file_name_img)
  plt.close()
  return file_name_img

  
  

def _notion_adicionar_ciclo_tipo_roleta(page_ciclo_tipo, titulo, prefixo, prefixo_arquivo, tipo_ciclo, qtde_ciclos):
  page_ciclo_prioridade = page_ciclo_tipo.children.add_new(PageBlock, title=titulo)
  newchild = page_ciclo_prioridade.children.add_new(EmbedOrUploadBlock, title=titulo)
  #file_name_img = "prioridade_ciclo_" + tipo_ciclo + "_" + qtde_ciclos + "_" + prefixo_arquivo + ".png"
  prefixo_arquivo_csv = prefixo + "_ciclo_" + tipo_ciclo + "_" + str(qtde_ciclos) + "__" + prefixo_arquivo
  try:
    file_name_img = image_consumo_recursos2(prefixo_arquivo_csv)
    print(file_name_img)
    newchild.upload_file(file_name_img)   
  except:
    print("Erro (image_consumo_recursos2): " + prefixo_arquivo_csv)  

  try:  
    file_name_img = image_qtde_ap_acumulado_por_ciclo2(prefixo_arquivo_csv)
    print(file_name_img)
    newchild = page_ciclo_prioridade.children.add_new(EmbedOrUploadBlock, title=titulo)
    newchild.upload_file(file_name_img)   
  except Exception as e: 
    print(e)
    traceback.print_exc()
    print("Erro (image_qtde_ap_acumulado_por_ciclo2): " + prefixo_arquivo_csv)  

  try:
    file_name_img = image_valor_ap_por_ciclo2(prefixo_arquivo_csv)
    print(file_name_img)
    newchild = page_ciclo_prioridade.children.add_new(EmbedOrUploadBlock, title=titulo)
    newchild.upload_file(file_name_img)   
  except:
    print("Erro (image_valor_ap_por_ciclo2): " + prefixo_arquivo_csv)  


def _notion_adicionar_ciclo_tipo(prefixo_arquivo, page_ciclo, titulo, tipo_ciclo, qtde_ciclos):
  page_ciclo_tipo = page_ciclo.children.add_new(PageBlock, title=titulo)

  _notion_adicionar_ciclo_tipo_roleta(page_ciclo_tipo, "Prioridade", "prioridade", prefixo_arquivo, tipo_ciclo, qtde_ciclos)
  _notion_adicionar_ciclo_tipo_roleta(page_ciclo_tipo, "Valor", "valor", prefixo_arquivo, tipo_ciclo, qtde_ciclos)
  _notion_adicionar_ciclo_tipo_roleta(page_ciclo_tipo, "Qtde", "qtde", prefixo_arquivo, tipo_ciclo, qtde_ciclos)
  _notion_adicionar_ciclo_tipo_roleta(page_ciclo_tipo, "Aleatória", "aleatoria", prefixo_arquivo, tipo_ciclo, qtde_ciclos)
  _notion_adicionar_ciclo_tipo_roleta(page_ciclo_tipo, "Custo/Benefício", "custobeneficio", prefixo_arquivo, tipo_ciclo, qtde_ciclos)
  if qtde_ciclos > 1:
    _notion_adicionar_ciclo_tipo_roleta(page_ciclo_tipo, "Todas Roletas", "todas_roletas", prefixo_arquivo, tipo_ciclo, qtde_ciclos)
    _notion_adicionar_ciclo_tipo_roleta(page_ciclo_tipo, "Todas Roletas Aleatórias", "todas_roletas_aleatorias", prefixo_arquivo, tipo_ciclo, qtde_ciclos)

  # page_ciclo_prioridade = page_ciclo_tipo.children.add_new(PageBlock, title="Prioridade")
  # newchild = page_ciclo_prioridade.children.add_new(EmbedOrUploadBlock, title="Prioridade")
  # #file_name_img = "prioridade_ciclo_" + tipo_ciclo + "_" + qtde_ciclos + "_" + prefixo_arquivo + ".png"
  # prefixo_arquivo_csv = "prioridade_ciclo_" + tipo_ciclo + "_" + str(qtde_ciclos) + "__" + prefixo_arquivo
  # file_name_img = image_consumo_recursos2(prefixo_arquivo_csv)
  # print(file_name_img)
  # newchild.upload_file(file_name_img)   
  # file_name_img = image_qtde_ap_acumulado_por_ciclo2(prefixo_arquivo_csv)
  # print(file_name_img)
  # newchild = page_ciclo_prioridade.children.add_new(EmbedOrUploadBlock, title="Prioridade")
  # newchild.upload_file(file_name_img)   
  # file_name_img = image_valor_ap_por_ciclo2(prefixo_arquivo_csv)
  # print(file_name_img)
  # newchild = page_ciclo_prioridade.children.add_new(EmbedOrUploadBlock, title="Prioridade")
  # newchild.upload_file(file_name_img)   


def _notion_adicionar_ciclo(prefixo_arquivo, page, titulo_ciclos, qtde_ciclos):
  page_ciclo = page.children.add_new(PageBlock, title=titulo_ciclos)
  _notion_adicionar_ciclo_tipo(prefixo_arquivo, page_ciclo, "Quantidade de ações", "acoes", qtde_ciclos)
  if qtde_ciclos > 1:
    _notion_adicionar_ciclo_tipo(prefixo_arquivo, page_ciclo, "Quantidade de recurso consumido", "recur", qtde_ciclos)


def teste_notion(prefixo):
    token_v2 = "9a07de97da77103b6b40ad24445a064c18f9e9a5a700154140104699b5971854aaffe9fc9dd4bc6aaa9858f7e883c7b053484adefdcde2d416ed38f6d8af110a6ba263a4025d1bb9a6b8bdb688dd"
    notion_client = NotionClient(token_v2=token_v2)

    #global notion_client
    #url="https://www.notion.so/24-05-2021-6d11acf4f3b44b868be082ddcacc21d4"

    url="https://www.notion.so/01-06-2021-969ff360498846af97221cfcd75a7bef"

    page = notion_client.get_block(url, limit=10)

    new_page = page.children.add_new(PageBlock, title=prefixo)

    _notion_adicionar_ciclo(prefixo, new_page, "1 ciclo", 1)
    _notion_adicionar_ciclo(prefixo, new_page, "5 ciclos", 5)
    _notion_adicionar_ciclo(prefixo, new_page, "10 ciclos", 10)
    # newchild = new_page.children.add_new(EmbedOrUploadBlock, title="resultado")
    # newchild.upload_file("prioridade_c1__qtde[1500.00 200.00 150.00 150.00]__prioridade[25.00 25.00 25.00 25.00]_consumo-recursos.png")    


#create_images('prioridade', prefixo)

#prefixo = "qtde[1500.00 200.00 150.00 150.00]__prioridade[25.00 25.00 25.00 25.00]"
#teste_notion(prefixo)

#q1500_200_150_150_p25_25_25_25


#prefixo = "qtde[1500.00 200.00 150.00 150.00]__prioridade[25.00 25.00 25.00 25.00]"
#prefixo = "qtde[500.00 500.00 500.00 500.00]__prioridade[60.00 10.00 10.00 10.00]"
if (len(sys.argv) < 2):
   sys.exit("Informe o nome do prefixo")

prefixo = sys.argv[1]

print("Vai iniciar: " + prefixo)
teste_notion(prefixo)


# teste_notion("qtde[1500.00 200.00 150.00 150.00]__prioridade[50.00 30.00 15.00 5.00]")
# teste_notion("qtde[1500.00 200.00 150.00 150.00]__prioridade[60.00 10.00 10.00 10.00]")
# teste_notion("qtde[500.00 500_500_500]__prioridade[50.00 30.00 15.00 5.00]")
# teste_notion("qtde[500.00 500_500_500]__prioridade[60.00 10.00 10.00 10.00]")

print("...fim...")
sys.exit()
#create_images('todas_roletas', prefixo)
create_images('prioridade', prefixo)
create_images('qtde', prefixo)
create_images('aleatoria',prefixo)
create_images('valor', prefixo)
create_images('custobeneficio', prefixo)



