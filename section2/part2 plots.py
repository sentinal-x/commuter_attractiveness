import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scaling import analysis

final_data = pd.read_csv('final_data.csv')

# Attractiveness
a = final_data['Attractiveness'].tolist()
# Population
p = final_data['Population'].tolist()
# Inbound Commuters
inbound = final_data['c_in'].tolist()
# Commute Impact Factor (a x p)
cif = (final_data['Attractiveness'] * final_data['Population']).tolist()

x_values = [('Attractiveness', a),('Population', p),('Inbound Commuters', inbound),('Commute Impact Factor (a x p)',cif)]

cda = final_data['Criminal Damage and Arson'].tolist()
cod = final_data['Crimes Of Dishonesty'].tolist()
so = final_data['Sexual Offences'].tolist()
vio = final_data['Violence'].tolist()
oc = final_data['Other'].tolist()
total = final_data['Total'].tolist()

y_values = [('Criminal Damage and Arson', cda), ('Crimes Of Dishonesty', cod), ('Sexual Offences', so), ('Violence', vio), ('Other Crimes', oc), ('Total Crimes', total)]
key = pd.read_csv('relationship_key.csv')
i = 0
for x in x_values:
    for y in y_values:
        data_xy = (x[1], y[1])
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
        plt.xlabel(x[0])
        plt.title(relationship)

        plt.show()

        print(beta, beta_ci)
        i += 1
