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
    Tf = random.randint(1, 2) # Teaching factor: either 1 or 2
 
    # for i=1 to Np
    for i in range (0, population_size -1):
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


    




