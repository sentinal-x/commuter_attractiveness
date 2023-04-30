import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scaling import analysis

commute = pd.read_csv('sorted_data.csv')
population = pd.read_csv('population_sorted.csv')
merge = commute.merge(population, left_on='Local Authority', right_on='Local Authority', how='inner')

# Attractiveness
c_in = merge['c_in'].tolist()
# Population
c_stay = merge['c_stay'].tolist()
# Inbound Commuters
c_out = merge['c_out'].tolist()

resident_workforce = (merge['c_stay'] + merge['c_out']).tolist()

# Commute Impact Factor (a x p)
p = merge['Population'].tolist()

y_values = [('Visitor Workforce (C_in)', c_in), ('C_stay', c_stay), ('C_out', c_out), ('Resident Workforce', resident_workforce)]
key = pd.read_csv('relationship_key.csv')

i = 24
for x in [p]:
    for y in y_values:
        data_xy = (x, y[1])
        data_xy = np.array(data_xy)
        rmodel = key.loc[i, 'best_model']
        relationship = key.loc[i, 'relationship']
        result = pd.read_csv(str(i) + '.csv')
        model_row = result[result['Model'] == rmodel]

        # Get the values of the columns in the filtered row
        beta = model_row['Beta'].iloc[0]
        beta_ci = model_row['Beta_CI'].iloc[0]
        bic = model_row['BIC'].iloc[0]
        alpha = model_row['Param1'].iloc[0]
        
        line = 10**np.linspace(np.log10(data_xy[0].min()*0.8), np.log10(data_xy[0].max()*1.2), len(x))
        mean = alpha*np.power(line, beta)

        plt.scatter(*data_xy, color='red', s=2.)
        plt.plot(line, mean, color='k')
        plt.xscale('log')
        plt.yscale('log')
        plt.ylabel(y[0])
        plt.xlabel('Population')
        plt.title(relationship)

        plt.show()

        print(beta, beta_ci)
        i += 1
