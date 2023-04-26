import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scaling import analysis

models = {'lognormal_delta_fixed': analysis.LogNormalFixedDAnalysis,
          'lognormal_delta_fixed_beta_fixed': analysis.LogNormalFixedDFixedBetaAnalysis,
          'lognormal': analysis.LogNormalAnalysis,
          'lognormal_beta_fixed': analysis.LogNormalFixedBetaAnalysis,
          'gaussian_delta_fixed': analysis.FixedDAnalysis,
          'gaussian_delta_fixed_beta_fixed': analysis.FixedDFixedBetaAnalysis,
          'gaussian': analysis.ConstrainedDAnalysis,
          'gaussian_beta_fixed': analysis.ConstrainedDFixedBetaAnalysis,
          'person': analysis.PopulationAnalysis,
          'person_beta_fixed': analysis.PopulationFixedGammaAnalysis}

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

i = 0
key_df = pd.DataFrame(columns=['key', 'relationship'])
for x in x_values:
    for y in y_values:
        data_xy = (x[1], y[1])
        relationship = (x[0]+' against '+y[0])
        results = []
        for m in models:
            model = models[m]
            r = model(data_xy, required_successes=50)
            beta, beta_ci = r.beta
            bic = r.bic
            params = list(r.params)
            pv = r.p_value
            row = {
                'Model': m,
                'Beta': beta,
                'Beta_CI': beta_ci,
                'BIC': bic,
                'P_Value': pv,
                'Param1': params[0],
                'Param2': params[1],
                'Param3': params[2],
                'Param4': params[3],
            }
            results.append(row)
            print(row)

        df = pd.DataFrame(results)
        sorted_df = df.sort_values(by='BIC')
        sorted_df.to_csv((i+'.csv'), index=False)
        key_df.append({'key': i, 'relationship': relationship}, ignore_index=True)
        i += 1

key_df.to_csv('relationship_key.csv', index=False)