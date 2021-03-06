import pandas as pd
import numpy as np
import random
import math
import sys

import yaml

from notion.client import *
from notion.block import *
from notion.collection import NotionDate
from numpy import inf, nan
from os.path import exists


def teste_notion():
    token_v2 = "9a07de97da77103b6b40ad24445a064c18f9e9a5a700154140104699b5971854aaffe9fc9dd4bc6aaa9858f7e883c7b053484adefdcde2d416ed38f6d8af110a6ba263a4025d1bb9a6b8bdb688dd"
    notion_client = NotionClient(token_v2=token_v2)

    #global notion_client
    url="https://www.notion.so/15-05-2021-674a71c39e5d4bc6ad00a3e6fec8576f"

    page = notion_client.get_block(url, limit=10)

    new_page = page.children.add_new(PageBlock, title="19/05/2021")
    newchild = new_page.children.add_new(EmbedOrUploadBlock, title="resultado")
    #newchild.upload_file("prioridade_c1__qtde[1500.00 200.00 150.00 150.00]__prioridade[25.00 25.00 25.00 25.00]_consumo-recursos.png")    

    newchild.upload_file("prioridade_ciclo_acoes_1__qtde[1500.00 200.00 150.00 150.00]__prioridade[25.00 25.00 25.00 25.00]_consumo-recursos.png")

# teste_notion()
# print("teste Notion finalizado")






# if (len(sys.argv) < 2):
#    sys.exit("Informe o nome do arquivo yaml")

# print('Number of arguments:'+ str(len(sys.argv))+ 'arguments.')
# print('Argument List:'+ str(sys.argv))
# yaml_file = open(sys.argv[1], 'r')


# yaml_file = open("ciclo_tempoacoes_12_q1500_200_150_150_p50_30_15_5.yaml")

yaml_file = open("ciclo_tempoacoes_12_q500_500_500_500_p50_30_15_5.yaml")


yaml_content = yaml.load(yaml_file)

print("Key: Value")
#print(type(yaml_content.items()))
for key, value in yaml_content.items():
    print(f"{key}: {value}")




print(yaml_content['population_size'])    


population_size =yaml_content['population_size'] #15 # Np 5
maximum_iterations = yaml_content['maximum_iterations']# 100 # T 10

decision_variables_count = yaml_content['decision_variables_count']#4
total_recurso_compartilhado = yaml_content['total_recurso_compartilhado']#10000
qtde_ciclos_recalcular_modelo = yaml_content['qtde_ciclos_recalcular_modelo']

tipo_ciclo = yaml_content['tipo_ciclo']

if (tipo_ciclo == ""):
  print("Informe o tipo de ciclo")
  quit()

   
qtde_recurso_consumido_para_recalcular_ciclo = math.ceil(total_recurso_compartilhado / qtde_ciclos_recalcular_modelo)
print(qtde_recurso_consumido_para_recalcular_ciclo)
# APs_qtdes = np.array([500, 20, 70, 60])
# APs_prioridades = np.array([35, 30, 20, 15])   

# APs_qtdes = np.array([500, 500, 500, 500])
# APs_prioridades = np.array([60, 10, 10, 10])  


# APs_qtdes = np.array([500, 500, 500, 500])
# APs_prioridades = np.array([25, 25, 25, 25])  

x_qtdes = list(yaml_content['APs_qtdes'].split(" "))
APs_qtdes =np.array(list(map(int,x_qtdes)), dtype=np.float32) 



total_qtde_APs = APs_qtdes.sum()
print(APs_qtdes)
print(total_qtde_APs)
qtde_APs_executadas_para_recalcular_modelo = math.ceil(total_qtde_APs / qtde_ciclos_recalcular_modelo)

if (tipo_ciclo =="tempo_acoes"):
   qtde_recurso_consumido_para_recalcular_ciclo = 0
   prefixo_tipo_ciclo="tempo_acoes"
elif (tipo_ciclo =="tempo_recursos"):
   qtde_APs_executadas_para_recalcular_modelo = 0
   prefixo_tipo_ciclo="tempo_recur"   
elif (tipo_ciclo =="qtde_acoes"):
   qtde_recurso_consumido_para_recalcular_ciclo = 0
   prefixo_tipo_ciclo="acoes"
elif (tipo_ciclo =="qtde_recursos"):
   qtde_APs_executadas_para_recalcular_modelo = 0
   prefixo_tipo_ciclo="recur"

x_prioridades = list(yaml_content['APs_prioridades'].split(" "))
APs_prioridades = np.array(list(map(int,x_prioridades)), dtype=np.float32) 

x_custos  = list(yaml_content['APs_custos'].split(" "))
APs_custos = np.array(list(map(float,x_custos)), dtype=np.float32) 
print(APs_prioridades)

prefixo = "ciclo_" + prefixo_tipo_ciclo +"_" + str(qtde_ciclos_recalcular_modelo) + "__qtde" + np.array2string(APs_qtdes, formatter={'float_kind':lambda x: "%.2f" % x}) + '__prioridade' + np.array2string(APs_prioridades, formatter={'float_kind':lambda x: "%.2f" % x})

all_bounds = np.empty((1, decision_variables_count), dtype=float)
#print(all_bounds)
 
def sortear_acao_positiva_prioridade():
   x = random.randint(1, 100)
   soma = 0
   index = 0
   for i in APs_prioridades:
     if APs_qtdes[index] > 0:
       soma = soma + i
     if x < soma:
        return index
     index = index + 1        

def sortear_acao_positiva_qtde():
   qtde = np.sum(APs_qtdes)
   x = random.randint(1, qtde)
   soma = 0
   index = 0
   for i in APs_qtdes:
     if APs_qtdes[index] > 0:
       soma = soma + i
     if x <= soma:
        return index
     index = index + 1     

def sortear_acao_positiva_valor(best):
   qtde = np.sum(best)
   #print("sortear_acao_positiva_valor: " + str(qtde))
   x = random.randint(1, qtde)
   soma = 0
   index = 0
   for i in best:
     if best[index] > 0:
       soma = soma + i
     if x <= soma:
        return index
     index = index + 1 

def sortear_acao_positiva_custo_beneficio(custo_beneficio):
   global APs_custos
   index_resultado = -1
   while index_resultado == -1: # enquanto n??o encontrou o resultado
     i = custo_beneficio.argmax()
     if APs_qtdes[i] == 0:
        custo_beneficio[i] = 0
     else:
        index_resultado = i
        return index_resultado
   
    

def sortear_acao_positiva_aleatoria():
   return random.randint(0, decision_variables_count -1)

def sortear_acao_positiva(tipo_roleta, best, custo_beneficio):
   #return sortear_acao_positiva_qtde()
   #return sortear_acao_positiva_prioridade()
   if (tipo_roleta == 'prioridade'):
      return sortear_acao_positiva_prioridade()
   elif (tipo_roleta == 'qtde'):
      return sortear_acao_positiva_qtde()
   elif (tipo_roleta == 'aleatoria'):   
      return sortear_acao_positiva_aleatoria()
   elif (tipo_roleta == 'valor'):   
      return sortear_acao_positiva_valor(best)
   elif (tipo_roleta == 'custobeneficio'):         
      return sortear_acao_positiva_custo_beneficio(custo_beneficio)
   else:
      print("Tipo de roleta inv??lida.".format(tipo_roleta))      

   #return sortear_acao_positiva_aleatoria()

def calcular_APs_bounds():
  i = 0
  resultado = np.empty((decision_variables_count, 1), dtype=float)

  for row in APs_qtdes:
      if row > 0:
        resultado[i] = (total_recurso_compartilhado / row)
        #print(resultado[i])

        ## com prioridade
        resultado[i] = ((total_recurso_compartilhado * (APs_prioridades[i]/100)) / row)
        #print(resultado[i])
        resultado[i] = math.ceil(resultado[i])
      else:
        resultado[i] = 0

      i = i + 1
  return resultado


#print("Limites:")
#print(APs_bounds)
#print(np.transpose(APs_bounds))

def calcular_lower_bound_(aIndex):
  prioridade = 0
  for i in range(aIndex + 1):
    prioridade = prioridade + APs_prioridades[i]
  
  resultado = APs_bounds[aIndex] - (APs_bounds[aIndex] * (prioridade / 100))
  #print(math.floor(resultado[0]))
  ##resultado = math.floor(resultado[0])
  resultado = resultado[0]
  if resultado == 0:
     resultado = 1
  return resultado

def calcular_lower_bound(aIndex):
   return 1


# (Learner phase: step 10) select a partner solution, it must be different of i
def select_partner_index(i):
    partner = random.randint(0, population_size - 1)
    while partner == i:
        partner = random.randint(0, population_size - 1)
    return partner

def fitness(x1, x2, x3, x4):
   #  x1 = (500 * x1)
   #  x2 = (20 * x2) 
   #  x3 = (70 * x3) 
   #  x4 = (60 * x4) 
    x1 = (APs_qtdes[0] * x1)
    x2 = (APs_qtdes[1] * x2) 
    x3 = (APs_qtdes[2] * x3) 
    x4 = (APs_qtdes[3] * x4) 


     #resultado = (500 * x1) + (20 * x2) + (70 * x3) + (60 * x4)
    resultado = x1 + x2 + x3 + x4
    resultado = (((resultado - total_recurso_compartilhado) ** 2) // ( total_recurso_compartilhado * 2) )
    return resultado

def fitness_row(row):

    return fitness(row[0], row[1], row[2], row[3])


def fitness_array(ar):
  num_rows, num_cols = ar.shape

  fitness = np.empty((num_rows, 1), dtype=float)

  i = 0
  for row in ar:
      frow = fitness_row(row)
      fitness[i, 0] = frow
      i = i + 1
  return fitness      


def verify_bound_item(value, lower_bound, upper_bound):
    if value < lower_bound:
        value = lower_bound
    elif value > upper_bound:
        value = upper_bound
    return value


def verify_bound(row):
   #  row[0] = round(verify_bound_item(row[0], 13, 20), 0) # 35% superior (20 * 0,65)
   #  row[1] = round(verify_bound_item(row[1], 175, 500), 0) # 35% + 20%superior (500 * 0,55)
   #  row[2] = round(verify_bound_item(row[2], 21, 142), 0) # 55 + 30% superior(500 * 0,85)   
   #  row[3] = round(verify_bound_item(row[3], 1, 106), 0)

   #  print(row[0])
   #  print(calcular_lower_bound(0))
   #  print(APs_bounds[0])

    item0 = verify_bound_item(row[0], calcular_lower_bound(0), APs_bounds[0])
    #print("item0: " + str(item0))
    if type(item0) == np.ndarray:
       item0 = item0[0]       
    row[0] = round(item0, 0) # 35% superior (20 * 0,65)
   #  print(row[1])
   #  print(calcular_lower_bound(1))
   #  print(APs_bounds[1])    
    item1 = verify_bound_item(row[1], calcular_lower_bound(1), APs_bounds[1])
    #print("item1: " + str(item1))
    if type(item1) == np.ndarray:
       item1 = item1[0]    
    row[1] = round(item1, 0) # 35% + 20%superior (500 * 0,55)
   #  print(row[2])
   #  print(calcular_lower_bound(2))
   #  print(APs_bounds[2])    
    item2 = verify_bound_item(row[2], calcular_lower_bound(2), APs_bounds[2])
    #print("item2: " + str(item2))
    if type(item2) == np.ndarray:
       item2 = item2[0]
    row[2] = round(item2, 0) # 55 + 30% superior(500 * 0,85)   
   #  print(row[3])
   #  print(calcular_lower_bound(3))
   #  print(APs_bounds[3])
    item3 = verify_bound_item(row[3], calcular_lower_bound(3), APs_bounds[3])
    #print("item3: " + str(item3))
    if type(item3) == np.ndarray:
       item3 = item3[0]    

    row[3] = round(item3, 0)    

    for i in range(0, decision_variables_count):
      if APs_qtdes[i] == 0:
         row[i] = 0    
   #  print(row[3])
   #  print(calcular_lower_bound(3))
   #  print(APs_bounds[3])    

    return row




def create_row():
    row = np.empty([0,0])

   #  row = np.append(row, round(random.randrange(13, 20), 2))
   #  row = np.append(row, round(random.randrange(175, 500), 2))
   #  row = np.append(row, round(random.randrange(21, 142), 2))
   #  row = np.append(row, round(random.randrange(1, 106), 2))

   

   #  row = np.append(row, round(random.randrange(calcular_lower_bound(0), APs_bounds[0][0]), 2))
   #  row = np.append(row, round(random.randrange(calcular_lower_bound(1), APs_bounds[1][0]), 2))
   #  row = np.append(row, round(random.randrange(calcular_lower_bound(2), APs_bounds[2][0]), 2))
   #  row = np.append(row, round(random.randrange(calcular_lower_bound(3), APs_bounds[3][0]), 2))
    for i in range(decision_variables_count):
      if APs_bounds[i][0] > 1:
         ##row = np.append(row, round(random.randrange(calcular_lower_bound(i), APs_bounds[i][0]), 2))
         row = np.append(row, round(random.randrange(math.floor(calcular_lower_bound(i)), math.floor(APs_bounds[i][0])), 2))
      else:
         row = np.append(row, 0)


    return row



def calcular_tlbo():

   global APs_bounds     
   global all_bounds 
   #2: Initialize a random population (P)
   # P = np.empty((0, decision_variables_count), int)

   # for i in range (0, population_size):
   #    P = np.vstack([P, create_row()])   

   # print(P)
   # print(type(P))

   # np.savetxt(r'populacao_inicial.csv',P,delimiter=',', fmt=('%f')) #, fmt=("%s, %f")

   # popula????o inicial P ser?? sempre a mesma
   P = np.genfromtxt ('populacao_inicial.csv', delimiter=",")

   #print(P)
   APs_bounds = calcular_APs_bounds()
   #print(APs_bounds)   
   all_bounds = np.vstack((all_bounds, np.transpose(APs_bounds)))   
   # print("Limites:")
   # print(all_bounds)

   # print("Limite:")
   # print(np.transpose(APs_bounds))

   # 3: Evaluate fitness of P
   f = fitness_array(P)
   # print("Popula????o Inicial:")
   # print(P)
   # print("Fitness Inicial:")
   # print(f)

   # 4: for t=1 to T
   for t in range (1, maximum_iterations):
      # for i=1 to Np
      Tf = random.randint(1, 2) # Teaching factor: either 1 or 2
   
      for i in range (0, population_size):
         ##### Teacher phase
         r = np.random.rand(1, decision_variables_count)

         Xi = P[i]

         # Choose Xbest 
         XBest_index = np.argmin(f, axis=None, out=None)
         XBest = P[XBest_index]
         XMean = np.mean(P, axis=0)
         XNew = Xi + r*(XBest - (Tf*XMean))
         # Bound Xnew and evaluate its fitness fnew
         XNew = verify_bound(XNew[0])
         fitness_xnew = fitness_row(XNew)
         fitness_xi = fitness_row(Xi)
         # Accept Xnew if its better than Xi
         if fitness_xnew < fitness_xi:
            P[i] = XNew

         ##### Learner phase
         # choose any solution randomly, Xp
         partner_index = select_partner_index(i)
         Xp = P[partner_index]
         fitness_Xp = fitness_row(Xp)
         fitness_xi = fitness_row(Xi)
         if fitness_xi < fitness_Xp:
            XNew = Xi + r*(Xi - Xp)
         else:
            XNew = Xi - r*(Xi - Xp)
         XNew = verify_bound(XNew[0])
         fitness_xnew = fitness_row(XNew)
         fitness_xi = fitness_row(Xi)

         # Accept Xnew if its better than Xi
         if fitness_xnew < fitness_xi:
            P[i] = XNew


   # print("Popula????o Solucao final:")
   # print(P)
   f = fitness_array(P)
   # print("Fitness final:")
   # print(f)

   XBest_index = np.argmin(f, axis=None, out=None)
   # print("Solu????o escolhida: {}".format(XBest_index))
   XBest = P[XBest_index]
   # print(XBest)
   # print("Fitness da solu????o escolhida: {}".format(fitness_row(P[XBest_index])))
   return XBest


#print(APs_qtdes)

# retorna a proxima roleta a ser utilizada
def proxima_roleta(roleta_atual):
   if roleta_atual == "":
      return 'custobeneficio'
   elif roleta_atual == 'custobeneficio':
      return 'valor'
   elif roleta_atual == 'valor':
      return 'prioridade'      
   elif roleta_atual == 'prioridade':
      return 'qtde'            
   elif roleta_atual == 'qtde':
      return 'aleatoria'
   elif roleta_atual == 'aleatoria':
      return 'custobeneficio'                        
 
def sortear_roleta():
   roletas=['custobeneficio', 'valor', 'prioridade', 'qtde', 'aleatoria']
   x = random.randint(0, len(roletas) -1)

   return roletas[x]


def simulacao_roleta(tipo_roleta):
   global total_recurso_compartilhado
   global all_bounds
   global APs_qtdes
   global APs_prioridades
   total_recurso_compartilhado = yaml_content['total_recurso_compartilhado']
   utilizacao_RCs = np.array([total_recurso_compartilhado])

   x_qtdes = list(yaml_content['APs_qtdes'].split(" "))
   APs_qtdes =np.array(list(map(int,x_qtdes)), dtype=np.float32) 
   x_prioridades = list(yaml_content['APs_prioridades'].split(" "))
   APs_prioridades =np.array(list(map(int,x_prioridades)), dtype=np.float32) 

   APs_bounds = calcular_APs_bounds()

   x_custos = list(yaml_content['APs_custos'].split(" "))
   APs_custos = np.array(list(map(float,x_custos)), dtype=np.float32) 

   tipo_roleta_src = tipo_roleta



   qtde_vezes_AP_executada = np.zeros(decision_variables_count)
#print(qtde_vezes_AP_executada)

   all_fitness = np.empty((1, decision_variables_count), dtype=float)
   all_qtde_vezes_AP_executada = np.empty((1, decision_variables_count), dtype=float)
   all_bounds = np.empty((1, decision_variables_count), dtype=float)
   all_bounds = np.delete(all_bounds, (0), axis=0)   
   all_custo_beneficio = np.empty((1, decision_variables_count), dtype=float)

   best = calcular_tlbo()
   print("{}....".format(tipo_roleta))

   #print(sortear_acao_positiva())
   qtde_APs_executadas_ciclo_atual = 1
   qtde_recurso_consumido_ciclo_atual = 0


   print("Qtde dispon??vel de cada AP: ") 
   print(APs_qtdes)
   print("Valor Unit??rio de cada AP: ")
   print(best)
   #print(all_fitness)
   all_fitness = np.vstack((all_fitness, best))
   #print(all_fitness)
   custo_beneficio = best / APs_custos
   all_custo_beneficio = np.vstack((all_custo_beneficio, custo_beneficio))

   # se vai usar todas as roletas, inicia com a custobeneficio
   if tipo_roleta_src == "todas_roletas":
      tipo_roleta = "custobeneficio"
   elif tipo_roleta_src == "todas_roletas_aleatorias":
      tipo_roleta = sortear_roleta()


   if prefixo_tipo_ciclo == "tempo_acoes":
      qtde_APs_executadas_para_recalcular_modelo_max = math.ceil(total_qtde_APs / qtde_ciclos_recalcular_modelo)
      qtde_APs_executadas_para_recalcular_modelo = random.randint(math.ceil(qtde_APs_executadas_para_recalcular_modelo_max / 2), qtde_APs_executadas_para_recalcular_modelo_max)
      print("Para o pr??ximo ciclo devem ser executadas {} a????es. Valor escolhido entre {} e {}".format(qtde_APs_executadas_para_recalcular_modelo, math.ceil(qtde_APs_executadas_para_recalcular_modelo_max / 2), qtde_APs_executadas_para_recalcular_modelo_max))

   count_ciclos = 1
   while total_recurso_compartilhado > 0:
      ap_disponivel = False
      if np.count_nonzero(APs_qtdes > 0) == 0:
         print("Fim das APs")
         break     
      

      while ap_disponivel == False:
         acao_positiva = sortear_acao_positiva(tipo_roleta, best, custo_beneficio)
         #print("AP sorteada {}".format(acao_positiva))
         if acao_positiva is not None:
            ap_disponivel = APs_qtdes[acao_positiva] > 0

      # diminui a a????o positiva executada
      if tipo_roleta_src == "todas_roletas_aleatorias":
         tipo_roleta = sortear_roleta()      

      qtde_vezes_AP_executada[acao_positiva] += 1
      APs_qtdes[acao_positiva] = APs_qtdes[acao_positiva]-1

      qtde = best[acao_positiva]
      # se terminou as quantidades dispon??veis da AP, zera o seu valor para n??o ser mais escolhido na roleta
      if (APs_qtdes[acao_positiva] == 0):
         best[acao_positiva] = 0      
         custo_beneficio[acao_positiva] = 0      
      qtde_recurso_consumido_ciclo_atual = qtde_recurso_consumido_ciclo_atual + qtde
      total_recurso_compartilhado = total_recurso_compartilhado - qtde
      #print("A????o executada: {}. Unidades monet??rias: {}. RC: {}. Roleta {} {}".format(acao_positiva, qtde, total_recurso_compartilhado, tipo_roleta, prefixo))
      if (qtde_ciclos_recalcular_modelo > 1) and \
         (((qtde_recurso_consumido_para_recalcular_ciclo > 0) and (qtde_recurso_consumido_ciclo_atual >= qtde_recurso_consumido_para_recalcular_ciclo)) or \
         ((qtde_APs_executadas_para_recalcular_modelo > 0) and (qtde_APs_executadas_ciclo_atual >= qtde_APs_executadas_para_recalcular_modelo))):
         print("Qtde de vezes que cada AP foi executada:")
         print(qtde_vezes_AP_executada)
         print("Qtde dispon??vel de cada AP: ")       
         print(APs_qtdes)
         print("RC: {}".format(total_recurso_compartilhado))
         utilizacao_RCs = np.vstack((utilizacao_RCs, total_recurso_compartilhado))
         print("")
         if (qtde_APs_executadas_para_recalcular_modelo > 0):
            print("Rec??lculo ap??s {} APs executadas".format(qtde_APs_executadas_ciclo_atual))
         else:
            print("Rec??lculo ap??s {} recursos consumidos".format(qtde_recurso_consumido_ciclo_atual))

         count_ciclos+=1
         if (count_ciclos > qtde_ciclos_recalcular_modelo):
            print("Fim da simula????o. J?? foram executados {} ciclos. Qtde ciclos a ser executados: {}.".format(count_ciclos-1, qtde_ciclos_recalcular_modelo))
            break
         print("Iniciando o ciclo {}. Qtde ciclos a ser executados: {}.".format(count_ciclos, qtde_ciclos_recalcular_modelo))           
         
         best = calcular_tlbo()
         for i in range(0, decision_variables_count):
            if APs_qtdes[i] == 0:
               best[i] = 0
         custo_beneficio = best / APs_custos
         all_custo_beneficio = np.vstack((all_custo_beneficio, custo_beneficio))
         all_fitness = np.vstack((all_fitness, best))

         all_qtde_vezes_AP_executada = np.vstack((all_qtde_vezes_AP_executada, qtde_vezes_AP_executada))

         if  tipo_roleta_src == "todas_roletas":
            tipo_roleta = proxima_roleta(tipo_roleta) # retorna a pr??xima roleta a ser utilizada

         if prefixo_tipo_ciclo == "tempo_acoes":
           qtde_APs_executadas_para_recalcular_modelo_max = math.ceil(total_qtde_APs / qtde_ciclos_recalcular_modelo)
           qtde_APs_executadas_para_recalcular_modelo = random.randint(math.ceil(qtde_APs_executadas_para_recalcular_modelo_max / 2), qtde_APs_executadas_para_recalcular_modelo_max)
           print("Para o pr??ximo ciclo devem ser executadas {} a????es. Valor escolhido entre {} e {}".format(qtde_APs_executadas_para_recalcular_modelo, math.ceil(qtde_APs_executadas_para_recalcular_modelo_max / 2), qtde_APs_executadas_para_recalcular_modelo_max))

         #print(all_fitness)

         qtde_APs_executadas_ciclo_atual = 0
         qtde_recurso_consumido_ciclo_atual = 0
         #print("......")
         # print(best)
         # print("Qtde dispon??vel de cada AP: ") 
         # print(APs_qtdes)

         # se ainda s?? possui 1 AP, ajusta manualmente o seu valor
         if np.count_nonzero(APs_qtdes > 0) == 1:
            best = total_recurso_compartilhado / APs_qtdes
            best = np.ceil(best)
            best[best == inf] = 0
            best[best == nan] = 0

         if np.count_nonzero(APs_qtdes > 0) == 0:
            print("Fim das APs")
            break


         print("Valor Unit??rio de cada AP: ")
         print(best)

      qtde_APs_executadas_ciclo_atual = qtde_APs_executadas_ciclo_atual + 1   

   # armazena dados do ??ltimo ciclo
   utilizacao_RCs = np.vstack((utilizacao_RCs, total_recurso_compartilhado))
   all_qtde_vezes_AP_executada = np.vstack((all_qtde_vezes_AP_executada, qtde_vezes_AP_executada))

   all_fitness = np.delete(all_fitness, (0), axis=0)
   print("Fitness:")
   print(len(all_fitness))
   print(all_fitness)

   
   all_qtde_vezes_AP_executada = np.delete(all_qtde_vezes_AP_executada, (0), axis=0)

   pd.DataFrame(all_fitness).to_csv("resultados/{}_{}_all_fitness.csv".format(tipo_roleta_src, prefixo))

   pd.DataFrame(all_qtde_vezes_AP_executada).to_csv("resultados/{}_{}_all_qtde_vezes_AP_executada.csv".format(tipo_roleta_src, prefixo))


#all_bounds = np.delete(all_bounds, (0), axis=0)
   print("Limites:")
   print(all_bounds)
   pd.DataFrame(all_bounds).to_csv("resultados/{}_{}_all_bounds.csv".format(tipo_roleta_src, prefixo))

   print("Utiliza????o do RC:")
   print(utilizacao_RCs)
   #utilizacao_RCs = np.delete(utilizacao_RCs, (0), axis=0)
   pd.DataFrame(utilizacao_RCs).to_csv("resultados/{}_{}_utilizacao_RCs.csv".format(tipo_roleta_src, prefixo))

   print("Custo/Benef??cio:")
   all_custo_beneficio = np.delete(all_custo_beneficio, (0), axis=0)
   print(all_custo_beneficio)
   pd.DataFrame(all_custo_beneficio).to_csv("resultados/{}_{}_custo_beneficio.csv".format(tipo_roleta_src, prefixo))



def executar_simulacoes():
   # print("Iniciando todas roletas...")
   # simulacao_roleta('todas_roletas')   
   # print("Iniciando roleta por custobeneficio...")
   # simulacao_roleta('custobeneficio')
   # print("Iniciando roleta por valor...")
   # simulacao_roleta('valor')
   # print("Iniciando todas roletas aleat??rias...")
   # simulacao_roleta('todas_roletas_aleatorias')   
   # print("Iniciando roleta por prioridade...")
   simulacao_roleta('prioridade')
   print("Iniciando roleta por qtde...")
   simulacao_roleta('qtde')
   print("Iniciando roleta aleat??ria...")
   simulacao_roleta('aleatoria')



executar_simulacoes()
print(".....fim.....")





