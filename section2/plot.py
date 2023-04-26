import pandas as pd

data = pd.read_csv('final_data.csv')

import matplotlib.pyplot as plt

x = data['Attractiveness'] * data['Population']
y = data['Total']

# Create scatter plot of Total against Attractiveness
plt.scatter(x, y)
plt.xscale('log')
plt.yscale('log')
plt.ylabel('Total Crimes')
plt.xlabel('PopulatAttrac')
plt.title('Total Crime vs c_in for Matching Locations')

# Display the plot
plt.show()