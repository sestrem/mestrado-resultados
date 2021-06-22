import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import style

sns.set()
style.use('ggplot')

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


fitness = pd.read_csv('all_fitness.csv', names=['x1', 'x2', 'x3', 'x4'], skiprows=1)
#create_image(fitness, 'Fitness', 'fitness.png')

qtde_vezes_AP = pd.read_csv('all_qtde_vezes_AP_executada.csv', names=['x1', 'x2', 'x3', 'x4'], skiprows=1)
#create_image(qtde_vezes_AP, 'Qtde vezes cada AP foi executada', 'qtde_vezes_AP_executada.png')

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


