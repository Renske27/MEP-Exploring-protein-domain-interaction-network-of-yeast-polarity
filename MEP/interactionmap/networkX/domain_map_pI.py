import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.colors import TwoSlopeNorm
import numpy as np

# Load the data
infile = 'C:/Users/rensk/PycharmProjects/MEP_codefiles/MEP/data/list2_data/interactionmap_data/domain_only_interactions_plDDT70_noscorethes_v2.csv'
domain_data = 'C:/Users/rensk/PycharmProjects/MEP_codefiles/MEP//data/list2_data/interactionmap_data/domains_info_2.csv'


# Load the domain data
domain_interactions_df = pd.read_csv(infile, sep='\t')
domain_info = pd.read_csv(domain_data, sep=',')

# Filter out rows where Domain1_Accession or Domain2_Accession is 'None'
filtered_df = domain_interactions_df[
    (domain_interactions_df['Domain1_Accession'] != 'None') &
    (domain_interactions_df['Domain2_Accession'] != 'None')
]

# Calculate average domain length and average pI for each domain accession
domain_info['domain_length'] = domain_info['domain_end'] - domain_info['domain_start'] + 1
average_domain_length = domain_info.groupby('domain_accession')['domain_length'].mean()
average_domain_pI = domain_info.groupby('domain_accession')['domain_pI'].mean()
domain_shortnames = domain_info.set_index('domain_accession')['domain_shortname'].to_dict()

# Manually normalize the pI values for the color map
def normalize_pI(pI, vmin=1, vmax=14, vcenter=6.8):
    if pI < vcenter:
        return (pI - vmin) / (vcenter - vmin) * 0.5
    else:
        return 0.5 + (pI - vcenter) / (vmax - vcenter) * 0.5

# Create a graph
G = nx.Graph()

# Add nodes for domains with size based on average domain length and color based on average pI
for domain in set(filtered_df['Domain1_Accession']).union(set(filtered_df['Domain2_Accession'])):
    pI = average_domain_pI.get(domain, 6.8)
    G.add_node(
        domain,
        size=average_domain_length.get(domain, 1) * 10,  # Multiply by 10 for better visualization
        color=plt.cm.bwr(normalize_pI(pI)),  # Map normalized pI to color
        label=domain_shortnames.get(domain, domain)  # Use domain_shortname as label
    )

# Add edges for domain interactions
for _, row in filtered_df.iterrows():
    domain1_accession = row['Domain1_Accession']
    domain2_accession = row['Domain2_Accession']
    count = row['Average_Interacting_Residues']

    # Add edge with interaction count as weight
    G.add_edge(domain1_accession, domain2_accession, weight=count)

# Get node attributes for plotting
node_sizes = [G.nodes[node]['size'] for node in G.nodes()]
node_colors = [G.nodes[node]['color'] for node in G.nodes()]
node_labels = {node: G.nodes[node]['label'] for node in G.nodes()}

# Draw the graph
pos = nx.spring_layout(G, k=2, iterations=25)  # You can adjust k and iterations for more or less spacing # You can experiment with other layouts like shell_layout, etc.
plt.figure(figsize=(30, 20))

# Draw nodes with sizes and colors based on the calculated attributes
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors)

# Draw edges with varying thickness based on interaction count
edges = G.edges(data=True)
for edge in edges:
    nx.draw_networkx_edges(G, pos, edgelist=[(edge[0], edge[1])], width=edge[2]['weight'] / 10)

# Draw labels using domain_shortname
nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=20)

# Add colorbar as a legend for the heatmap
sm = plt.cm.ScalarMappable(cmap='coolwarm', norm=plt.Normalize(vmin=1, vmax=14))
sm.set_array([])
cbar = plt.colorbar(sm)
cbar.set_label('Domain pI', fontsize=20)

# Set the font size of colorbar ticks
cbar.ax.tick_params(labelsize=18)

# Set fontsize for the title
plt.title('Domain Interaction Map with Domain Sizes and pI Heatmap', fontsize=28)

# Create a custom legend for line thickness (interaction count)
legend_lines = [
    Line2D([0], [0], color='black', lw=10/10, label='Count: 10'),
    Line2D([0], [0], color='black', lw=50/10, label='Count: 50'),
    Line2D([0], [0], color='black', lw=100/10, label='Count: 100')
    # Line2D([0], [0], color='black', lw=200/10, label='Count: 200'),
    # Line2D([0], [0], color='black', lw=300/10, label='Count: 300')
]

# Add the legend to the plot
plt.legend(handles=legend_lines, title='Average Interacting Residues (Edge Thickness)', fontsize=18, title_fontsize=20)

# Show the plot
plt.show()
