import pandas as pd

# Load the CSV file into a pandas dataframe
crime_data = pd.read_csv('crime.csv')

crime_data.columns = crime_data.columns.str.strip()
crime_data['Number of Offences'] = crime_data['Number of Offences'].str.replace(',', '')
crime_data['Number of Offences'] = pd.to_numeric(crime_data['Number of Offences'], errors='coerce')

# Check that the 'Number of Offences' column exists in the dataframe
if 'Number of Offences' not in crime_data.columns:
    raise ValueError('Column "Number of Offences" not found in the dataframe')

# Group the data by location, CSP Name, Offence Group, and Offence Subgroup,
# then sum up the number of offences for each group
crime_totals = crime_data.groupby(['CSP Name', 'Offence Group'])['Number of Offences'].sum().reset_index()

# Print out the total number of offences for each group at each location
# Pivot the data to create a table with CSP Name as the index, Offence Groups as the columns, and Total Number of Offences as the values
crime_pivot = crime_totals.pivot(index='CSP Name', columns='Offence Group', values='Number of Offences')

# Add a column for the total number of crimes for each CSP Name
crime_pivot['Total'] = crime_pivot.sum(axis=1)

# Export the data to a CSV file
crime_pivot.to_csv('crime_totals.csv', index=True)