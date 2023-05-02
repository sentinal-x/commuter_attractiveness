import pandas as pd

data = pd.read_csv('final_data.csv')

import matplotlib.pyplot as plt

y = data['Attractiveness'] 
x = data['c_stay + c_out']

# Create scatter plot of Total against Attractiveness
plt.scatter(x, y)
plt.xscale('log')
plt.yscale('log')
plt.ylabel('Attractiveness')
plt.xlabel('Resident Workforce')
plt.title('Resident Workforce vs Attractiveness for Matching Locations')

# Display the plot
plt.show()