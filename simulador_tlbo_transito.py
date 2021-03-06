import numpy as np
import random
import math

population_size = 15 # Np 5
maximum_iterations = 100 # T 10

decision_variables_count = 4

total_recurso_compartilhado = 10000

APs_qtdes = np.array([500, 20, 70, 60])
APs_prioridades = np.array([35, 30, 20, 15])

def sortear_acao_positiva():
   x = random.randint(1, 100)
   soma = 0
   index = 0
   for i in APs_prioridades:
     if APs_qtdes[index] > 0:
       soma = soma + i
     if x < soma:
        return index
     index = index + 1        


def calcular_APs_bounds():
  i = 0
  resultado = np.empty((decision_variables_count, 1), dtype=float)

  for row in APs_qtdes:
      if row > 0:
        resultado[i] = math.floor(total_recurso_compartilhado / row)
      else:
        resultado[i] = 0

      i = i + 1
  return resultado


APs_bounds = calcular_APs_bounds()
#print(APs_bounds)

def calcular_lower_bound(aIndex):
  prioridade = 0
  for i in range(aIndex + 1):
    prioridade = prioridade + APs_prioridades[i]
  
  resultado = APs_bounds[aIndex] - (APs_bounds[aIndex] * (prioridade / 100))
  #print(math.floor(resultado[0]))
  resultado = math.floor(resultado[0])
  if resultado == 0:
     resultado = 1
  return resultado


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
         row = np.append(row, round(random.randrange(calcular_lower_bound(i), APs_bounds[i][0]), 2))
      else:
         row = np.append(row, 0)


    return row



def calcular_tlbo():
   #2: Initialize a random population (P)
   P = np.empty((0, decision_variables_count), int)

   for i in range (0, population_size):
      P = np.vstack([P, create_row()])

   global APs_bounds      

   APs_bounds = calcular_APs_bounds()

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


print(APs_qtdes)
best = calcular_tlbo()
print("......")

#print(sortear_acao_positiva())
qtde_acoes_executadas = 0

print("Qtde dispon??vel de cada AP: ") 
print(APs_qtdes)
print("Valor Unit??rio de cada AP: ")
print(best)
while total_recurso_compartilhado > 0:
   ap_disponivel = False
   while ap_disponivel == False:
     acao_positiva = sortear_acao_positiva()
     #print("AP sorteada {}".format(acao_positiva))
     if acao_positiva is not None:
       ap_disponivel = APs_qtdes[acao_positiva] > 0
   # diminui a a????o positiva executada
   APs_qtdes[acao_positiva] = APs_qtdes[acao_positiva]-1
   qtde = best[acao_positiva]
   total_recurso_compartilhado = total_recurso_compartilhado - qtde
   print("A????o executada: {}. Unidades monet??rias: {}. RC: {}".format(acao_positiva, qtde, total_recurso_compartilhado))
   if qtde_acoes_executadas == 10:
      print("Rec??lculo ap??s 10 APs executadas")
      #print(APs_qtdes)
      best = calcular_tlbo()
      qtde_acoes_executadas = 0
      #print("......")
      #print(best)
      print("Qtde dispon??vel de cada AP: ") 
      print(APs_qtdes)
      print("Valor Unit??rio de cada AP: ")
      print(best)

   qtde_acoes_executadas = qtde_acoes_executadas + 1   






