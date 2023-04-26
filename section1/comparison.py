import pandas as pd

df1 = pd.read_csv('sorted_data.csv')
df2 = pd.read_csv('crime_totals_scot.csv')

# Find matching locations
matching_locations = df1.merge(df2, left_on='Local Authority', right_on='CSP Name', how='inner')
print('Matching locations:')
print(matching_locations)

import matplotlib.pyplot as plt

# Create scatter plot of Total against Attractiveness
plt.scatter(matching_locations['Total'], matching_locations['Attractiveness'])

# Add axis labels and title
plt.xlabel('Total Crimes')
plt.ylabel('Attractiveness')
plt.title('Total vs Attractiveness for Matching Locations')

# Display the plot
plt.show()

# Find non-matching locations
locations_1 = set(df1['Local Authority'])
locations_2 = set(df2['CSP Name'])
non_matching_locations = list(locations_1.symmetric_difference(locations_2))
print('Non-matching locations:')
print(non_matching_locations)