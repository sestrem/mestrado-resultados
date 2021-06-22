import numpy as np
import random


population_size = 5 # Np
maximum_iterations = 10 # T

decision_variables_count = 4

# (Learner phase: step 10) select a partner solution, it must be different of i
def select_partner_index(i):
    partner = random.randint(0, population_size - 1)
    while partner == i:
        partner = random.randint(0, population_size - 1)
    return partner



def fitness(x1, x2, x3, x4):
    resultado = (500 * x1) + (20 * x2) + (70 * x3) + (60 * x4)
    resultado = (((resultado - 10000) ** 2) // 10000)
    return resultado

def fitness_row(row):
    # print(row)
    # print(row[0])
    # print(row[1])
    # print(row[2])
    # print(row[3])
    return fitness(row[0], row[1], row[2], row[3])


def fitness_array(ar):
  num_rows, num_cols = ar.shape

  #fitness  = np.empty((num_rows, 1), int)
  fitness = np.empty((num_rows, 1), dtype=float)

  i = 0
  for row in ar:
      frow = fitness_row(row)
    #   print(frow)
    #   print(fitness)
      #fitness = np.hstack([fitness, fitness_row(row)])
      fitness[i, 0] = frow
      i = i + 1
  return fitness      


def verify_bound_item(value, lower_bound, upper_bound):
    #print(value)
    if value < lower_bound:
        value = lower_bound
    elif value > upper_bound:
        value = upper_bound
    return value

def verify_bound(row):
    row[0] = round(verify_bound_item(row[0], 1, 20), 0)
    row[1] = round(verify_bound_item(row[1], 1, 500), 0)
    row[2] = round(verify_bound_item(row[2], 1, 142), 0)    
    row[3] = round(verify_bound_item(row[3], 1, 106), 0)

    return row

def create_row():
    row = np.empty([0,0])

    row = np.append(row, round(random.randrange(0, 20), 2))
    row = np.append(row, round(random.randrange(0, 500), 2))
    row = np.append(row, round(random.randrange(0, 142), 2))
    row = np.append(row, round(random.randrange(0, 106), 2))
    return row

#2: Initialize a random population (P)
P = np.empty((0, decision_variables_count), int)

# for i in range (0, population_size -1):
P = np.vstack([P, create_row()])
P = np.vstack([P, create_row()])
P = np.vstack([P, create_row()])
P = np.vstack([P, create_row()])
P = np.vstack([P, create_row()])
print("População Inicial:")
print(P)

# 3: Evaluate fitness of P
f = fitness_array(P)
print("Fitness Inicial:")
print(f)

# 4: for t=1 to T
for t in range (1, maximum_iterations):
    # for i=1 to Np
    Tf = random.randint(1, 2) # Teaching factor: either 1 or 2
 
    for i in range (0, population_size -1):
       ##### Teacher phase
       r = np.random.rand(1, decision_variables_count)
    #    print(r)

       Xi = P[i]
    #    print(Xi)

       # Choose Xbest 
       XBest_index = np.argmin(f, axis=None, out=None)
    #    print(XBest_index)
       XBest = P[XBest_index]
    #    print(XBest)
       XMean = np.mean(P, axis=0)
    #    print(XMean)
       XNew = Xi + r*(XBest - (Tf*XMean))
    #    print(XNew)
       # Bound Xnew and evaluate its fitness fnew
       XNew = verify_bound(XNew[0])
    #    print(XNew)
       fitness_xnew = fitness_row(XNew)
       fitness_xi = fitness_row(Xi)
       # Accept Xnew if its better than Xi
       if fitness_xnew < fitness_xi:
        #    print("--Teacher Phase-- T: {}, i: {}".format(t, i))
        #    print(P)
        #    print("New P")
           P[i] = XNew
        #    print(P)
        #    print(".........")

       # Continuar...
       ##### Learner phase
       # choose any solution randomly, Xp
       partner_index = select_partner_index(i)
    #    print("partner_index: {}".format(partner_index))
       Xp = P[partner_index]
    #    print("Xp:")
    #    print(Xp)
       fitness_Xp = fitness_row(Xp)
       fitness_xi = fitness_row(Xi)
    #    print("fitness_Xp: {}".format(fitness_Xp))
    #    print("fitness_xi: {}".format(fitness_xi))
       if fitness_xi < fitness_Xp:
        #    print("Xi: ")
        #    print(Xi)
        #    print("r: ")
        #    print(r)
        #    print("Xp: ")
        #    print(Xp)                      
           XNew = Xi + r*(Xi - Xp)
        #    print("XNew: ")
        #    print(XNew)                      
       else:
        #    print("Xi: ")
        #    print(Xi)
        #    print("r: ")
        #    print(r)
        #    print("Xp: ")
        #    print(Xp) 
           XNew = Xi - r*(Xi - Xp)
        #    print("XNew: ")
        #    print(XNew)                      
       XNew = verify_bound(XNew[0])
    #    print("XNew:")
    #    print(XNew)
       fitness_xnew = fitness_row(XNew)
       fitness_xi = fitness_row(Xi)
    #    print("fitness_xnew: {}".format(fitness_xnew))
    #    print("fitness_xi: {}".format(fitness_xi))

       # Accept Xnew if its better than Xi
       if fitness_xnew < fitness_xi:
        #    print("--Learner Phase-- T: {}, i: {}".format(t, i))
        #    print(P)
        #    print("New P")
           P[i] = XNew
        #    print(P)
        #    print(".........")



#print(fitness(5, 100, 60, 20))    
print("População Solucao final:")
print(P)
f = fitness_array(P)
print("Fitness final:")
print(f)

XBest_index = np.argmin(f, axis=None, out=None)
print("Solução escolhida: {}".format(XBest_index))
XBest = P[XBest_index]
print(XBest)
print("Fitness da solução escolhida: {}".format(fitness_row(P[XBest_index])))


    




