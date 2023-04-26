import csv
import math
import networkx as nx
import numpy as np
from geopy.geocoders import Nominatim
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import geopandas as gpd
import random

os.environ['SSL_CERT_FILE'] = 'cacert.cer'\

threshold = 100

if os.path.isfile('gb.shp'):
    uk = gpd.read_file('gb.shp')

    # Read the CRS of the shapefile
    crs = uk.crs

def plot_seperate_communities(comm):
    # Plot the shapefile
    fig, ax = plt.subplots(figsize=(5, 9))
    uk.plot(ax=ax, color='white', edgecolor='black')

    # Get subgraph for community
    subgraph = G.subgraph(comm)

    # Compute edge colours based on node weights
    node_weights = {}
    for node in subgraph.nodes:
        node_weights[node] = sum([subgraph.edges[(node, neighbor)]['weight'] for neighbor in subgraph.neighbors(node)])
    edge_colours = {}
    for u, v, data in subgraph.edges(data=True):
        opacity = math.sqrt(data['weight'] / node_weights[u])
        edge_colours[(u, v)] = (0, 0, 0, opacity)

    # Draw the subgraph
    nx.draw_networkx_nodes(subgraph, pos, node_color='blue', node_size=10)
    nx.draw_networkx_edges(subgraph, pos, edge_color=list(edge_colours.values()), arrows=True)
    nx.draw_networkx_labels(subgraph, pos, labels=nx.get_node_attributes(subgraph, 'city'), font_size=8)
    ax.set_position([0.1, 0.1, 0.8, 0.8])

    plt.show()

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
                G.add_edge(i, j-1, weight=float(data[i][j]))
    
    # Check if pos.csv exists and read it if it does
    if os.path.isfile('pos.csv'):
        print("pos.csv found")
        with open('pos.csv', newline='') as f:
            reader = csv.reader(f)
            pos = {int(row[0]): (float(row[1]), float(row[2])) for row in reader}
    
    else:
        quit

    # Remove self-loops from adjacency matrix
    for i in range(len(G)):
        G[i][i]['weight'] = 0
    
    nx.set_node_attributes(G, pos, 'pos')

    print('Graph Created...')
    
    return G

# Create the graph
G = create_graph_from_csv('A.csv')
pos = nx.get_node_attributes(G, 'pos')

# run the Louvain Community Detection Algorithm
communities = list(nx.community.louvain_communities(G, weight='weight', resolution = 0.6))

# Define color map for the communities
num_communities = len(communities)
cm = plt.get_cmap('gist_rainbow')
c_colors = [colors.rgb2hex(cm(1. * i / num_communities)) for i in range(num_communities)]
random.shuffle(c_colors)

# Plot the shapefile
fig, ax = plt.subplots(figsize=(5, 8))
uk.plot(ax=ax, color='white', edgecolor='black')

# Plot each subgraph with community color
legend_dict = {}
for i, comm in enumerate(communities):
    cities = [G.nodes[node]['city'] for node in comm]
    print(f'Community {i+1}: {", ".join(cities)}')

    # Get subgraph for community
    subgraph = G.subgraph(comm)

    # Compute edge colours based on node weights
    node_weights = {}
    for node in subgraph.nodes:
        node_weights[node] = sum([subgraph.edges[(node, neighbor)]['weight'] for neighbor in subgraph.neighbors(node)])

    # Draw the subgraph with community color
    nx.draw_networkx_nodes(subgraph, pos, node_color=c_colors[i], node_size=40)
    nx.draw_networkx_edges(subgraph, pos, edge_color=c_colors[i], arrows=True)

    # Add community index to legend dictionary
    legend_dict[f'Community {i+1}'] = c_colors[i]

# Create legend
ax.legend(handles=[mpatches.Patch(color=color, label=label) for label, color in legend_dict.items()], fontsize=3)

plt.show()

