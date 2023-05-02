import pandas as pd
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
# Resident Commuters
resident = final_data['c_stay + c_out'].tolist()
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

i = 28
key = []
for x in [('Resident Commuters', resident)]:
    for y in y_values:
        data_xy = (x[1], y[1])
        relationship = (x[0]+' against '+y[0])
        print(str(i) + ': ' + relationship)
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
                'Param1': params[0] if len(params) >= 1 else "",
                'Param2': params[1] if len(params) >= 2 else "",
                'Param3': params[2] if len(params) >= 3 else "",
                'Param4': params[3] if len(params) >= 4 else "",
            }
            results.append(row)
            print(row)

        df = pd.DataFrame(results)
        sorted_df = df.sort_values(by='BIC')
        sorted_df.to_csv((str(i)+'.csv'), index=False)
        best_model = sorted_df.loc[0, 'Model']
        key.append({'key': str(i), 'relationship': relationship, 'best_model': best_model})
        i += 1

key_df = pd.DataFrame(key)
key_df.to_csv('relationship_key2.csv', index=False)