import csv
import pandas as pd
import matplotlib.pyplot as plt

with open('A.csv', 'r') as file:
    reader = csv.reader(file)
    data = list(reader)

rowsums = []
for i in range(1, len(data)):
    row_sum = 0
    for j in range(1, len(data)):
        row_sum += int(data[i][j])
    rowsums.append(row_sum)

threshold = 100
colsums = []
diversity = [0] * len(data)
for i in range(1, len(data)):
    col_sum = 0
    for j in range(1, len(data)):
        if i != j:
            commuters = int(data[j][i])
            col_sum += commuters
            if commuters > threshold:
                diversity[i] += 1
    colsums.append(col_sum)

a_list = []
dataframe = []
for val in range(len(colsums)):
    a = colsums[val]/rowsums[val]
    a_list.append(a)
    name = data[val + 1][0]
    dataframe.append([name, a, colsums[val], rowsums[val], diversity[val]])

df = pd.DataFrame(dataframe, columns=['Local Authority', 'Attractiveness', 'c_in', 'c_stay + c_out', 'Diversity'])

# Create scatter plot of Total against Attractiveness
plt.scatter(df['Diversity'], df['Attractiveness'])

# Add axis labels and title
plt.xlabel('Diversity')
plt.ylabel('Attractiveness')
plt.title('Diversity vs Attractiveness')

# Display the plot
plt.show()

df_sorted = df.sort_values(by='Local Authority')
population = pd.read_csv('population_sorted.csv')
merge = df_sorted.merge(population, left_on='Local Authority', right_on='Local Authority', how='inner')

plt.scatter(merge['Diversity'], merge['Attractiveness'] * merge['Population'])

# Add axis labels and title
plt.xlabel('Diversity')
plt.ylabel('Attractiveness x Population')
plt.title('Diversity vs Attractiveness x Population')

# Display the plot
plt.show()

# export the sorted DataFrame as a csv file
df_sorted.to_csv('sorted_data.csv', index=False)