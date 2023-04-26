import csv
import math
import networkx as nx
from geopy.geocoders import Nominatim
import pyproj
import matplotlib.pyplot as plt
import os
import geopandas as gpd

os.environ['SSL_CERT_FILE'] = 'cacert.cer'

threshold = 400

if os.path.isfile('gb.shp'):
    uk = gpd.read_file('gb.shp')
    # Read the CRS of the shapefile
    crs = uk.crs

else:
    print('shapefile not found')
    quit()

# Define the function to read the CSV file and create the networkx graph
def create_graph_from_csv(csv_file):
    # Read the CSV file
    with open(csv_file, newline='') as f:
        reader = csv.reader(f)
        data = [row for row in reader][1:] # Skip the first row
        
    # Create the networkx graph
    G = nx.DiGraph() # Use DiGraph instead of Graph to create a directed graph
    
    # Add nodes with their city labels
    for i in range(len(data)):
        G.add_node(i, city=data[i][0])
        
    for i in range(len(data)):
        for j in range(len(data[i])):
            if j > 0 and int(data[i][j]) > threshold:
                G.add_edge(i, j-1, distance=float(data[i][j]))
    
    # Check if pos.csv exists and read it if it does
    if os.path.isfile('pos.csv'):
        print("pos.csv found")
        with open('pos.csv', newline='') as f:
            reader = csv.reader(f)
            pos = {int(row[0]): (float(row[1]), float(row[2])) for row in reader}
    else:
        # Get the geographic coordinates of the cities and write them to pos.csv
        geolocator = Nominatim(user_agent="ECM3401")
        pos = {}
        with open('pos.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for i in range(len(data)):
                print(data[i][0])
                location = geolocator.geocode(data[i][0] + ", United Kingdom")
                print(location)
                
                # Transform the latitude and longitude to the CRS of the shapefile
                transformer = pyproj.Transformer.from_crs('EPSG:4326', crs, always_xy=True)
                x, y = transformer.transform(location.longitude, location.latitude)
                
                pos[i] = (x, y)
                print(pos[i])
                writer.writerow([i, pos[i][0], pos[i][1]])
    
    nx.set_node_attributes(G, pos, 'pos')

    print('Graph Created...')
    
    return G

# Create the graph

if os.path.isfile('A.csv'):
    G = create_graph_from_csv('A.csv')
else:
    print("Commute data not found.")
    quit()

pos = nx.get_node_attributes(G, 'pos')

# Plot the shapefile
fig, ax = plt.subplots(figsize=(5, 9))
uk.plot(ax=ax, color='white', edgecolor='black')

node_weights = {}
for node in G.nodes:
    node_weights[node] = sum([G.edges[(node, neighbor)]['distance'] for neighbor in G.neighbors(node)])

edge_colours = {}
for u, v, data in G.edges(data=True):
    opacity = math.sqrt(data['distance'] / node_weights[u])
    edge_colours[(u, v)] = (0, 0, 0, opacity)

# Draw the graph
nx.draw_networkx_nodes(G, pos, node_color='blue', node_size = 10)
#nx.draw_networkx_edges(G, pos, edge_color=list(edge_colours.values()), arrows=True)
nx.draw_networkx_labels(G, pos, labels=nx.get_node_attributes(G, 'city'), font_size=8)

edge_list = [(u, v, data) for u, v, data in G.edges(data=True) if u != v]

# Draw the edges without self-loops
nx.draw_networkx_edges(G, pos, edgelist=edge_list, edge_color=list(edge_colours.values()), arrows=True)
ax.set_position([0.1, 0.1, 0.8, 0.8])

plt.show()
