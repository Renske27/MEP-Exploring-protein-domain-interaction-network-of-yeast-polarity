import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from netgraph import Graph
from matplotlib.patches import Circle
import numpy as np

# Load the data
domains_info = pd.read_csv(
    'C:/Users/rensk/PycharmProjects/MEP_codefiles/MEP/data/list2_data/interactionmap_data/domains_info.csv',
    delimiter=','
)
domain_contacts = pd.read_csv(
    'C:/Users/rensk/PycharmProjects/MEP_codefiles/MEP/data/list2_data/interactionmap_data/domain_contacts_plDDT70_noscorethres.csv',
    delimiter='\t'
)

# Create a graph and map domains to their respective proteins
G = nx.Graph()
node_to_community = {}

for _, row in domains_info.iterrows():
    unique_id = row['domain_accession'] + row['protein_accession']
    G.add_node(unique_id, domain=row['domain_accession'], protein=row['protein_accession'], label=row['domain_shortname'])
    node_to_community[unique_id] = row['protein_accession']

# Add edges between interacting domains
for _, row in domain_contacts.iterrows():
    if row['Domain1_Accession'] != 'None' and row['Domain2_Accession'] != 'None':
        unique_id1 = row['Domain1_Accession'] + row['Protein1_Accession']
        unique_id2 = row['Domain2_Accession'] + row['Protein2_Accession']
        interaction_strength = row['Count']
        G.add_edge(unique_id1, unique_id2, weight=interaction_strength)

# Generate color maps for domains and proteins
# Extract colors from the Accent, Set1, and Set2 colormaps
accent_colors = plt.cm.Accent(np.linspace(0, 1, plt.cm.Accent.N))
set1_colors = plt.cm.Set1(np.linspace(0, 1, plt.cm.Set1.N))
# Extract the first 6 colors from the Set2 colormap
set2_colors = plt.cm.Set2(np.linspace(0, 1, plt.cm.Set2.N))
# Select the first 3 colors and the 5th, 6th, and 7th colors
set2_selectedcolors = set2_colors[[0, 1, 2, 4, 5, 6]]
set3_colors= plt.cm.Set3(np.linspace(0, 1, plt.cm.Set3.N))[:6]
tab20_colors = plt.cm.tab20((np.linspace(0, 1, plt.cm.tab20.N)))
# Combine the colors into a single array
combined_colors = np.vstack([tab20_colors, set2_selectedcolors])
# Create a custom colormap using the combined colors
custom_cmap = mcolors.ListedColormap(combined_colors, name='custom_combined')

domain_palette = custom_cmap(np.linspace(0, 1, len(domains_info['domain_accession'].unique())))
protein_colors = plt.get_cmap('tab20').colors

proteins = domains_info['protein_accession'].unique()
domains = domains_info['domain_accession'].unique()
domain_colormap = {domain: domain_palette[i % len(domain_palette)] for i, domain in enumerate(domains)}
protein_colormap = {protein: protein_colors[i % len(protein_colors)] for i, protein in enumerate(proteins)}

# Map node colors based on the domain accession to which they belong
node_color = {node: domain_colormap[G.nodes[node]['domain']] for node in G.nodes()}

# Map node colors based on the protein to which they belong
node_color_protein = {node: protein_colormap[protein] for node, protein in node_to_community.items()}

# Create a colormap for the edges going from light grey to black
cmap = plt.cm.Greys  # Greyscale colormap
norm = plt.Normalize(vmin=min(nx.get_edge_attributes(G, 'weight').values()),
                     vmax=max(nx.get_edge_attributes(G, 'weight').values()))

# Draw the graph
plt.figure(figsize=(40, 30))
ax = plt.gca()

# Create the legend for domains
handles_domains = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=domain_colormap[domain], markersize=20)
    for domain in domains
]
legend1 = ax.legend(handles_domains, domains_info['domain_shortname'].unique(), title='Domains', loc='upper left',
                    fontsize=24, title_fontsize=32, bbox_to_anchor=(-0.17, 1))  # Legend placed inside, upper left
ax.add_artist(legend1)  # Manually add the first legend

# Create a second legend for the proteins
handles_proteins = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=protein_colormap[protein], markersize=20)
    for protein in proteins  # Add iteration over proteins here
]
legend2 = ax.legend(handles_proteins, domains_info['protein_input_name'].unique(), title='Proteins', loc='upper right',
                    fontsize=24, title_fontsize=32, bbox_to_anchor=(1.17, 1))

# Adjust the layout to make space for the legends
plt.subplots_adjust(left=0.2, right=0.8)

# Create a colormap for the edges going from darker grey to black
def truncate_colormap(cmap, minval=0.3, maxval=1.0, n=100):
    new_cmap = mcolors.LinearSegmentedColormap.from_list(
        'truncated', cmap(np.linspace(minval, maxval, n))
    )
    return new_cmap

# Truncate the colormap to exclude the lightest greys
cmap = truncate_colormap(plt.cm.Greys, minval=0.25, maxval=1.5)  # Start from a darker grey
norm = plt.Normalize(vmin=min(nx.get_edge_attributes(G, 'weight').values()),
                     vmax=max(nx.get_edge_attributes(G, 'weight').values()))

# Generate the edge colors based on the interaction strength (weights)
edge_colors = {
    (u, v): cmap(norm(G[u][v]['weight'])) for u, v in G.edges()
}
# Increase the spacing between communities by modifying the layout kwargs
graph = Graph(
    G,
    node_color=node_color, node_edge_width=0, edge_alpha=1, node_size=8,
    node_layout='community', node_layout_kwargs=dict(node_to_community=node_to_community),  # adjust scale to space out
    edge_color=edge_colors, edge_layout='curved', scale=(4.8, 4.8)
)

# Access node positions using the correct attribute
pos = graph.node_positions

# Add a color bar for edge color
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)  # ScalarMappable to create the colorbar
sm.set_array([])  # Empty array for ScalarMappable

# Create colorbar (without fontsize parameter)
cbar = plt.colorbar(sm, ax=ax, orientation='horizontal', fraction=0.05, pad=0.02)

# Set the label for the colorbar and its font size
cbar.set_label('Interaction Strength', fontsize=32)

# Set the font size for the tick labels on the color bar
cbar.ax.tick_params(labelsize=24)

# Add circles around communities and keep track of text positions for protein names
for protein in proteins:
    # Get the positions of all nodes in this community
    community_nodes = [node for node, p in node_to_community.items() if p == protein]
    community_positions = np.array([pos[node] for node in community_nodes])

    # Calculate the center of the community and the radius
    center = np.mean(community_positions, axis=0)
    max_distance = np.max(np.linalg.norm(community_positions - center, axis=1))

    # Draw a circle around the community using the corrected protein color map
    circle = Circle(center, max_distance + 0.15, color=protein_colormap[protein], fill=True, alpha=0.5)
    ax.add_patch(circle)

plt.title('Community Interaction Map (Proteins and Domains)', fontsize=38)

plt.show()
